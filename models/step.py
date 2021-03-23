from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship, Session

from models.bind_user import BindUser
from models.db import Base
from models.solution import Solution
from models.step_problem import StepProblem
from models.step_user import StepUser


class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=64))
    source = Column(String(length=32))

    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", backref="steps")


def get_step_solutions(step: Step, db: Session):
    # 查询该计划所有的绑定账号
    bind_query = (
        select(BindUser.id)
        .join(StepUser, BindUser.user_id == StepUser.user_id)
        .where(StepUser.step_id == step.id)
    )
    problem_query = select(StepProblem.problem_id).where(StepProblem.step_id == step.id)
    # 查找该计划所有绑定账号中在指定 step 中存在的题目的提交
    solutions: List[Solution] = (
        db.query(Solution)
        .filter(
            Solution.bind_user_id.in_(bind_query),
            Solution.problem_id.in_(problem_query),
        )
        # 提交时间从久到新
        .order_by(Solution.submitted_at)
        .all()
    )
    resp = {}
    for solution in solutions:
        bind_user_id = solution.bind_user_id
        if bind_user_id not in resp:
            resp[bind_user_id] = []
        resp[bind_user_id].append(solution)
    return resp
