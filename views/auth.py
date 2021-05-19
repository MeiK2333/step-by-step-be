import aiohttp
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import CLIENT_ID, CLIENT_SECRET
from logger import module_logger
from models.db import get_db
from models.user import User
from schemas.auth import create_access_token, Auth, get_current_auth, verify_password, get_password_hash
from schemas.exception import SBSException

router = APIRouter()
logger = module_logger("auth")


@router.get("/user/{username}")
def user_detail(username: str, db: Session = Depends(get_db)):
    data = {"steps": [], "bind_users": []}
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise SBSException(errmsg="User not found!")
    data["username"] = user.username
    data["robot"] = user.robot
    for usr in user.step_users:
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
    user = User(username=request.username, hashed_password=get_password_hash(request.password))
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
