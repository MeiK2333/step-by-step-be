from datetime import datetime

import aiohttp
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from config import CLIENT_ID, CLIENT_SECRET
from logger import module_logger
from models.bind_user import BindUser
from models.db import get_db
from models.group import Group
from models.source import Source
from models.step import Step, get_step_solutions
from models.step_problem import StepProblem
from models.step_user import StepUser
from models.user import User
from schemas.auth import create_access_token, Auth, get_current_auth, get_current_admin
from schemas.enums import ResultEnum
from schemas.exception import SBSException, exception_handler

logger = module_logger("stepbystep")

app = FastAPI()


app.add_exception_handler(SBSException, exception_handler)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/groups")
def group_list(db: Session = Depends(get_db)):
    groups = db.query(Group).filter().all()
    return groups


@app.get("/group/{group_id}/steps")
def group_steps(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).get(group_id)
    steps = group.steps
    rst = []
    for step in steps:
        prob = db.query(StepProblem).filter_by(step=step).count()
        usr = db.query(StepUser).filter_by(step=step).count()
        rst.append(
            {
                "id": step.id,
                "name": step.name,
                "source": step.source,
                "problemCount": prob,
                "userCount": usr,
            }
        )
    return rst


@app.get("/group/{group_id}")
def group_detail(group_id: int, db: Session = Depends(get_db)):
    return db.query(Group).get(group_id)


@app.get("/step/{step_id}")
def step_detail(step_id: int, db: Session = Depends(get_db)):
    step = db.query(Step).get(step_id)
    prob = db.query(StepProblem).filter_by(step=step).order_by(StepProblem.order).all()
    problems = []
    for pro in prob:
        problems.append(
            {
                "id": pro.problem.id,
                "order": pro.order,
                "project": pro.project,
                "topic": pro.topic,
                "problem": pro.problem.problem_id,
                "link": pro.problem.link,
                "title": pro.problem.title,
            }
        )
    usr = db.query(StepUser).filter_by(step=step).all()

    # 获取该 step 的所有提交
    solutions = get_step_solutions(step, db)
    users = []
    for step_usr in usr:
        bind_users = step_usr.user.bind_users
        user_all_solutions = []
        user_step_solutions = {}
        # 获取该用户所有绑定账号的提交
        for bind_user in bind_users:
            bind_user_id = bind_user.id
            if bind_user_id in solutions:
                user_all_solutions.extend(solutions[bind_user_id])
        # 如果已经 AC，则后续不再处理
        # 如果没有 AC，则取最新的状态
        for solution in user_all_solutions:
            if (
                user_step_solutions.get(solution.problem_id, {}).get("result")
                == "Accepted"
            ):
                continue
            if solution.submitted_at:
                date = solution.submitted_at.strftime("%Y-%m-%d")
            else:
                date = datetime.now().strftime("%Y-%m-%d")
            user_step_solutions[solution.problem_id] = {
                "result": "Accepted"
                if solution.result == ResultEnum.Accepted
                else "WrongAnswer",
                "date": date,
            }
        users.append(
            {
                "id": step_usr.user.id,
                "nickname": step_usr.nickname,
                "username": step_usr.user.username,
                "class": step_usr.clazz,
                "solutions": user_step_solutions,
            }
        )
    data = {"problems": problems, "users": users, "name": step.name}

    return data


@app.get("/user/{username}")
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
            }
        )
    for usr in user.bind_users:
        data["bind_users"].append(
            {"source": usr.source.name, "username": usr.username, "link": usr.link}
        )
    return data


@app.get("/login")
async def login(code: str = None, db: Session = Depends(get_db)):
    if not code:
        raise SBSException(errmsg="请提供 Code")
    # 总超时时间 10S
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                "https://github.com/login/oauth/access_token",
                json={
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": code,
                },
                headers={"accept": "application/json"},
            ) as resp:
                body = await resp.json()
                if "error" in body:
                    raise SBSException(errmsg=body["error"])
                access_token = body["access_token"]
            async with session.get(
                "https://api.github.com/user",
                headers={
                    "accept": "application/json",
                    "Authorization": f"token {access_token}",
                },
            ) as resp:
                user_dict = await resp.json()
    except Exception as ex:
        logger.warn(repr(ex))
        raise SBSException(errmsg="与认证服务器连接受限，请稍后重试")

    if not user_dict:
        raise SBSException(errmsg="System error!")
    access_token = create_access_token(user_dict, db=db)
    logger.info(f"github login: {user_dict}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=Auth)
async def read_users_me(current_auth: Auth = Depends(get_current_auth)):
    roles = current_auth.roles
    return current_auth


@app.delete("/group/{group_id}")
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    db.query(Group).filter_by(id=group_id).delete()
    db.commit()
    return {}


class EditGroupRequest(BaseModel):
    id: int
    name: str
    code: str


@app.put("/group/{group_id}")
def edit_group(
    group_id: int,
    request: EditGroupRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    group = db.query(Group).get(group_id)
    if not group:
        raise SBSException(errmsg="group not found")
    group.name = request.name
    group.code = request.code
    db.add(group)
    db.commit()
    return {}


class NewGroupRequest(BaseModel):
    name: str
    code: str


@app.post("/group")
def new_group(
    request: NewGroupRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    group = Group(name=request.name, code=request.code)
    db.add(group)
    db.commit()
    return group


class EditStepRequest(BaseModel):
    id: int
    name: str


@app.put("/group/{group_id}/step/{step_id}")
def edit_step(
    group_id: int,
    step_id: int,
    request: EditStepRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    group = db.query(Group).get(group_id)
    step = db.query(Step).get(step_id)
    if step.group != group:
        raise SBSException("how dare you")
    step.name = request.name
    db.add(step)
    db.commit()
    return {}


@app.delete("/group/{group_id}/step/{step_id}")
def delete_step(
    group_id: int,
    step_id: int,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    group = db.query(Group).get(group_id)
    step = db.query(Step).get(step_id)
    if step.group != group:
        raise SBSException("how dare you")
    db.query(Step).filter_by(id=step_id).delete()
    db.commit()
    return {}


class NewStepRequest(BaseModel):
    name: str


@app.post("/group/{group_id}/step")
def new_step(
    group_id: int,
    request: NewStepRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    group = db.query(Group).get(group_id)
    step = Step(name=request.name)
    step.group = group
    step.name = request.name
    db.add(step)
    db.commit()
    return {}


@app.get("/step/{step_id}/users")
def step_users(step_id: int, db: Session = Depends(get_db)):
    resp = []
    for step_user in db.query(StepUser).filter_by(step_id=step_id).all():
        step_user: StepUser
        bind_users = step_user.user.bind_users
        item = {
            "id": step_user.id,
            "class": step_user.clazz,
            "nickname": step_user.nickname,
            "bind_users": [],
        }
        for bind_user in bind_users:
            bind_user: BindUser
            item["bind_users"].append(
                {
                    "username": bind_user.username,
                    "link": bind_user.link,
                    "source": bind_user.source.name,
                }
            )
        resp.append(item)

    return resp


@app.delete("/group/{group_id}/step/{step_id}/user/{step_user_id}")
def delete_step_user(
    group_id: int,
    step_id: int,
    step_user_id: int,
    db: Session = Depends(get_db),
    _current_auth: Auth = Depends(get_current_admin),
):
    """ 从指定的计划中删除指定的用户，注意，这并不会修改已绑定的账号关系（只是从当前计划中移除） """
    step_user = db.query(StepUser).get(step_user_id)
    db.delete(step_user)
    db.commit()
    return {}


class NewStepUserRequest(BaseModel):
    username: str
    nickname: str
    clazz: str = Field(None, alias="class")
    source: str


@app.post("/group/{group_id}/step/{step_id}/user")
def new_step(
    group_id: int,
    step_id: int,
    request: NewStepUserRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    # TODO: 此处的逻辑需要明确整理一下
    group = db.query(Group).get(group_id)
    step = db.query(Step).get(step_id)
    if step.group != group:
        raise SBSException(errmsg="how dare you!")
    step_user: StepUser = (
        db.query(StepUser)
        .filter_by(nickname=request.nickname, clazz=request.clazz, step=step)
        .first()
    )
    source = db.query(Source).filter_by(name=request.source).first()
    if not source:
        raise SBSException(errmsg="Source 不存在！")
    if step_user:
        # 如果该计划已有该用户
        # 如果与之前的 source 不同，则为该用户添加一条 bind
        # 否则直接报错
        for bind_user in step_user.user.bind_users:
            bind_user: BindUser
            if bind_user.source == source:
                raise SBSException(errmsg="该用户已存在")
        # 如果该绑定不存在，则创建
        bind_user = db.query(BindUser).filter_by(source=source, username=request.username).first()
        if not bind_user:
            bind_user = BindUser()
            bind_user.source = source
            bind_user.username = request.username
        bind_user.user = step_user.user
        db.add(bind_user)
        db.commit()
        return {}
    # 管理员导入的账号会自动创建一个用户
    username = source.name + "-" + request.username
    user = db.query(User).filter_by(username=username).first()
    if not user:
        user = User()
        user.robot = True
        user.username = username
        db.add(user)
        db.commit()
        bind_user = BindUser()
        bind_user.source = source
        bind_user.username = request.username
        bind_user.user = user
        db.add(bind_user)
        db.commit()

    step_user = StepUser()
    step_user.user = user
    step_user.nickname = request.nickname
    step_user.clazz = request.clazz
    step_user.step = step
    db.add(step_user)
    db.commit()
    return {}
