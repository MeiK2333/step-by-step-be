from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from logger import module_logger
from models.bind_user import BindUser
from models.db import get_db
from models.source import Source
from models.step_user import StepUser
from models.user import User
from schemas.auth import (
    create_access_token,
    Auth,
    get_current_auth,
    verify_password,
    get_password_hash,
)
from schemas.exception import SBSException
from spider.poj.bind_user import login as poj_login
from spider.sdut.bind_user import login as sdut_login
from spider.vj.bind_user import login as vj_login

router = APIRouter()
logger = module_logger("auth")


class BindUserRequest(BaseModel):
    source: str
    username: str
    password: str


@router.post("/user/bind_user")
async def user_bind_user(
    request: BindUserRequest,
    current_auth: Auth = Depends(get_current_auth),
    db: Session = Depends(get_db),
):
    """
    从对应平台验证用户身份，然后绑定账号到当前用户
    """

    if request.source == "SDUT":
        resp = await sdut_login(request.username, request.password)
        if resp["success"] is False:
            raise SBSException(errmsg="用户名或密码错误")
    elif request.source == "VJ":
        resp = await vj_login(request.username, request.password)
        if not resp:
            raise SBSException(errmsg="用户名或密码错误")
    elif request.source == "POJ":
        resp = await poj_login(request.username, request.password)
        if not resp:
            raise SBSException(errmsg="用户名或密码错误")
    else:
        raise SBSException(errmsg="未知的平台")

    source = db.query(Source).filter_by(name=request.source).first()
    bind_user = (
        db.query(BindUser).filter_by(username=request.username, source=source).first()
    )
    if bind_user:
        # 如果已经被另一个真人绑定，则报错
        if bind_user.user.robot is False:
            raise SBSException(errmsg=f"此账号已经被 {bind_user.user.username} 绑定")
        # 如果关联了系统导入的账号，则将该账号所有数据移动到当前账号下，主要是绑定账号和参加的计划
        logger.info(f"移动 {bind_user.user.username} 到 {current_auth.username}")
        user = bind_user.user
        db.query(BindUser).filter_by(user_id=user.id).update(
            {BindUser.user_id: current_auth.id}
        )
        db.query(StepUser).filter_by(user_id=user.id).update(
            {StepUser.user_id: current_auth.id}
        )
        db.commit()
    else:
        # 创建一个 bind_user 并绑定到当前用户
        bind_user = BindUser(
            user=current_auth, source=source, username=request.username
        )
        db.add(bind_user)
        db.commit()
    return resp


@router.get("/user/{username}")
def user_detail(username: str, db: Session = Depends(get_db)):
    data = {"steps": [], "bind_users": []}
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise SBSException(errmsg="User not found!")
    data["username"] = user.username
    data["robot"] = user.robot
    for usr in user.step_users:
        if not usr.step:
            continue
        data["steps"].append(
            {
                "id": usr.step.id,
                "name": usr.step.name,
                "nickname": usr.nickname,
                "class": usr.clazz,
                "group": usr.step.group,
            }
        )
    for usr in user.bind_users:
        data["bind_users"].append(
            {"source": usr.source.name, "username": usr.username, "link": usr.link}
        )
    return data


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if user:
        raise SBSException(errmsg="该用户已存在")
    if (not 0 < len(request.username) < 1024) or (not request.username.isalnum()):
        raise SBSException(errmsg="校验错误")
    user = User(
        username=request.username, hashed_password=get_password_hash(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {}


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise SBSException(errmsg="用户名或密码错误")
    access_token = create_access_token(user, db=db)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=Auth)
async def read_users_me(current_auth: Auth = Depends(get_current_auth)):
    roles = current_auth.roles
    return current_auth
