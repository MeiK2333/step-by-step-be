from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from logger import module_logger
from models.bind_user import BindUser
from models.db import get_db
from models.group import Group
from models.problem import Problem
from models.source import Source
from models.step import Step
from models.step_problem import StepProblem
from models.step_user import StepUser
from models.user import User
from schemas.auth import Auth, get_current_admin
from schemas.exception import SBSException

router = APIRouter()
logger = module_logger("admin")


@router.delete("/group/{group_id}")
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    logger.info(f'{current_auth.username}: delete group {group_id}')
    db.query(Group).filter_by(id=group_id).delete()
    db.commit()
    return {}


class EditGroupRequest(BaseModel):
    id: int
    name: str
    code: str


@router.put("/group/{group_id}")
def edit_group(
    group_id: int,
    request: EditGroupRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    logger.info(f'{current_auth.username}: update group {group_id} to {request.json()}')
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


@router.post("/group")
def new_group(
    request: NewGroupRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    logger.info(f'{current_auth.username} create group {request.json()}')
    group = Group(name=request.name, code=request.code)
    db.add(group)
    db.commit()
    return group


class EditStepRequest(BaseModel):
    id: int
    name: str


@router.put("/group/{group_id}/step/{step_id}")
def edit_step(
    group_id: int,
    step_id: int,
    request: EditStepRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    logger.info(f'{current_auth.username} update step {step_id} to {request.json()}')
    group = db.query(Group).get(group_id)
    step = db.query(Step).get(step_id)
    if step.group != group:
        raise SBSException("how dare you")
    step.name = request.name
    db.add(step)
    db.commit()
    return {}


@router.delete("/group/{group_id}/step/{step_id}")
def delete_step(
    group_id: int,
    step_id: int,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    logger.info(f'{current_auth.username} delete step {step_id}')
    group = db.query(Group).get(group_id)
    step = db.query(Step).get(step_id)
    if step.group != group:
        raise SBSException("how dare you")
    db.query(StepUser).filter_by(step_id=step_id).delete()
    db.query(StepProblem).filter_by(step_id=step_id).delete()
    db.query(Step).filter_by(id=step_id).delete()
    db.commit()
    return {}


class NewStepRequest(BaseModel):
    name: str


@router.post("/group/{group_id}/step")
def new_step(
    group_id: int,
    request: NewStepRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    logger.info(f'{current_auth.username} create step {group_id} {request.json()}')
    group = db.query(Group).get(group_id)
    step = Step(name=request.name)
    step.group = group
    step.name = request.name
    db.add(step)
    db.commit()
    return {}


@router.get("/step/{step_id}/users")
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


@router.get("/step/{step_id}/problems")
def step_problems(step_id: int, db: Session = Depends(get_db)):
    resp = []
    for step_problem in (
        db.query(StepProblem)
        .filter_by(step_id=step_id)
        .order_by(StepProblem.order)
        .all()
    ):
        step_problem: StepProblem
        problem = step_problem.problem
        source = problem.source
        resp.append(step_problem)
    return resp


@router.delete("/group/{group_id}/step/{step_id}/user/{step_user_id}")
def delete_step_user(
    group_id: int,
    step_id: int,
    step_user_id: int,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    """ 从指定的计划中删除指定的用户，注意，这并不会修改已绑定的账号关系（只是从当前计划中移除） """
    logger.info(f'{current_auth.username} delete step {step_id} user {step_user_id}')
    db.query(StepUser).filter_by(id=step_user_id).delete()
    db.commit()
    return {}


class NewStepUserRequest(BaseModel):
    username: str
    nickname: str
    clazz: str = Field(None, alias="class")
    source: str


@router.post("/group/{group_id}/step/{step_id}/user")
def new_step_user(
    group_id: int,
    step_id: int,
    request: NewStepUserRequest,
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    """
    为计划添加 step_user 与其对应的 user 的 bind_user
    提交的请求中信息有：
        1. step_user（step、class、nickname）
        2. bind_user（source、username）
    我们需要做的是：为该 step_user 找到对应的 user，并为该 user 添加 bind_user 的绑定
    找对应 user 的顺序如下
    1. 如果 step_user 已存在，则 user 为 step_user.user
    2. 如果 step_user 不存在
        1. 如果 bind_user 存在，则 user 为 bind_user.user
        2. 无 user，需要自动生成


    1. 首先查找 user
        1. 如果同一个 step_user（step、class、nickname 都相同，认为是同一个 step_user）存在，则 user 为 step_user.user
        2. 如果该 step_user 不存在
            1. 查找 bind_user 是否已经存在（source、username 相同）
                1. 如果 bind_user 存在，则 user 为 bind_user.user
                2. 如果 bind_user 不存在，则创建一个新的 user
    2. 添加 step_user 与 user 的绑定，step_user.user = user
    3. 使用信息中的 source 与 username 查找 bind_user
        1. 如果 bind_user 不存在，则创建它
    4. 添加 user 与 bind_user 的关联，注意一个 bind_user 只能被一个 user 关联，即若该 bind_user 之前已经与其他 user 绑定，则此操作失败
    """
    logger.info(f'{current_auth.username} add user {request.json()} to step {step_id}')
    # 检查参数
    group = db.query(Group).get(group_id)
    step = db.query(Step).get(step_id)
    if step.group != group:
        raise SBSException(errmsg="how dare you!")
    source = db.query(Source).filter_by(name=request.source).first()
    if not source:
        raise SBSException(errmsg="Source 不存在！")

    step_user: StepUser = (
        db.query(StepUser)
        .filter_by(nickname=request.nickname, clazz=request.clazz, step=step)
        .first()
    )
    bind_user: BindUser = (
        db.query(BindUser).filter_by(source=source, username=request.username).first()
    )

    # 首先查找 User
    if step_user:
        user = step_user.user
    else:
        if bind_user:
            user = bind_user.user
        else:
            # 创建新的通过后台导入的 User
            import_username = f"{source.name}-{step.id}-{request.username}"
            user = db.query(User).filter_by(username=import_username).first()
            if not user:
                user = User()
                user.username = import_username
                user.robot = True
                db.add(user)
                db.commit()

    # 然后为 User 添加 bind_user 绑定
    if bind_user:
        # 如果已有 bind_user 且该 bind_user 已经绑定了其他人
        if bind_user.user != user:
            raise SBSException(
                errmsg=f"账号 {request.username} 已经被 {bind_user.user.username} 绑定，导入失败！"
            )
        else:  # 此时该账号已有一个相同的 bind_user，无需进行绑定操作
            pass
    else:  # 如果没有 bind_user，则创建
        bind_user = BindUser()
        bind_user.source = source
        bind_user.user = user
        bind_user.username = request.username
        db.add(bind_user)
        db.commit()

    # 最后为该 User 添加当前 step 的 step_user 绑定
    if step_user:
        # 如果已有 step_user 且该 step_user 已经绑定了其他人
        if step_user.user != user:
            raise SBSException(errmsg=f"理论上这个错误永远不会出现，如果你见到这个错误，请联系管理员～")
        else:  # 无需处理
            pass
    else:  # 如果没有 step_user，则创建
        step_user = StepUser(
            nickname=request.nickname, clazz=request.clazz, step=step, user=user
        )
        db.add(step_user)
        db.commit()

    return step_user


class EditStepProblemRequest(BaseModel):
    project: Optional[str]
    topic: Optional[str]
    problem: str
    source: str


@router.put("/group/{group_id}/step/{step_id}/problems")
def edit_step_problems(
    group_id: int,
    step_id: int,
    request: List[EditStepProblemRequest],
    db: Session = Depends(get_db),
    current_auth: Auth = Depends(get_current_admin),
):
    """
    为计划添加题目，将会全量覆盖之前的数据
    如果题目还不存在，则打印警告并创建该题目
    """
    logger.info(f'{current_auth.username} update step problems')
    for pro in request:
        logger.info(f'{pro.json()}')
    # 检查参数
    group = db.query(Group).get(group_id)
    step = db.query(Step).get(step_id)
    if step.group != group:
        raise SBSException(errmsg="how dare you!")
    problems = []
    for item in request:
        source = db.query(Source).filter_by(name=item.source).first()
        if not source:
            raise SBSException(errmsg="Source not found!")
        problem: Problem = db.query(Problem).filter_by(
            source=source, problem_id=item.problem
        ).first()
        if not problem:
            logger.warning(f"未知的题目！{item.source} - {item.problem}")
            problem = Problem()
            problem.source = source
            problem.problem_id = item.problem
            db.add(problem)
            db.commit()
        problems.append(problem)

    # 首先清除该计划之前的题目
    db.query(StepProblem).filter_by(step=step).delete()
    db.commit()

    for idx, problem in enumerate(problems):
        step_problem = StepProblem()
        step_problem.order = idx
        step_problem.step = step
        step_problem.problem = problem
        step_problem.project = request[idx].project
        step_problem.topic = request[idx].topic
        db.add(step_problem)
        db.commit()
    return {}
