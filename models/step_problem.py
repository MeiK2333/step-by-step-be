from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.db import Base
from models.problem import Problem


class StepProblem(Base):
    __tablename__ = "step_problem"
    id = Column(Integer, primary_key=True, index=True)

    project = Column(String(length=64), nullable=True, comment="专项")
    topic = Column(String(length=64), nullable=True, comment="专题")
    order = Column(Integer)

    problem_id = Column(Integer, ForeignKey("problems.id"))
    problem = relationship(Problem, backref="steps")

    step_id = Column(Integer, ForeignKey("steps.id", ondelete='CASCADE'))
    step = relationship("Step", backref="problems")
