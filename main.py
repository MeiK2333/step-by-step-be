from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models.db import get_db
from models.group import Group
from models.step import Step, get_step_solutions
from models.step_problem import StepProblem
from models.step_user import StepUser
from models.user import User
from schemas.enums import ResultEnum

app = FastAPI()


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
