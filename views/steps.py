from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.db import get_db
from models.step import Step, get_step_solutions
from models.step_problem import StepProblem
from models.step_user import StepUser
from schemas.enums import ResultEnum

router = APIRouter()


@router.get("/step/{step_id}")
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
