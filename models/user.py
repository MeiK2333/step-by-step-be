from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, select, Boolean
from sqlalchemy.orm import Session

from models.bind_user import BindUser
from models.db import Base
from models.problem import Problem
from models.solution import Solution, ResultEnum
from models.step import Step
from models.step_problem import StepProblem


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)

    robot = Column(Boolean, default=False)


def get_step_solutions(user: User, step: Step, db: Session):
    # 查询该用户所有的绑定账号
    bind_query = select(BindUser.id).where(BindUser.user == user)
    problem_query = (
        select(Problem.id).join(StepProblem).where(StepProblem.step == step)
    )
    # 查找该用户所有绑定账号中在指定 step 中存在的题目的提交
    solutions: List[Solution] = (
        db.query(Solution)
        .filter(
            Solution.bind_user_id.in_(bind_query), Solution.problem_id.in_(problem_query)
        )
        # 提交时间从久到新
        .order_by(Solution.submitted_at)
        .all()
    )

    resp = {}
    # 如果已经 AC，则后续不再处理
    # 如果没有 AC，则取最新的状态
    for solution in solutions:
        if resp.get(solution.problem_id, {}).get("result") == "Accepted":
            continue
        if solution.submitted_at:
            date = solution.submitted_at.strftime("%Y-%m-%d")
        else:
            date = datetime.now().strftime("%Y-%m-%d")
        resp[solution.problem_id] = {
            "result": "Accepted"
            if solution.result == ResultEnum.Accepted
            else "WrongAnswer",
            "date": date,
        }
    return resp
