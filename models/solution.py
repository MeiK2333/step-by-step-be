from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from models.db import Base
from models.problem import Problem
from models.source import Source
from schemas.enums import ResultEnum, LanguageEnum


class Solution(Base):
    __tablename__ = "solutions"
    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(length=64), index=True)
    nickname = Column(String(length=64))
    result = Column(Enum(ResultEnum))
    time_used = Column(Integer)
    memory_used = Column(Integer)
    code_len = Column(Integer)
    language = Column(Enum(LanguageEnum))
    submitted_at = Column(DateTime)

    bind_user_id = Column(Integer, ForeignKey("bind_user.id"))
    bind_user = relationship("BindUser", backref="solutions")

    problem_id = Column(Integer, ForeignKey("problems.id"))
    problem = relationship(Problem, backref="solutions")

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, backref="steps")
