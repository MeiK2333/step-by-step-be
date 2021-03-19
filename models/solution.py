import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from models.db import Base
from models.problem import Problem
from models.source import Source


class ResultEnum(enum.Enum):
    Accepted = 1
    WrongAnswer = 2
    # ...
    Unknown = 999


class LanguageEnum(enum.Enum):
    C = 1
    Cpp = 2
    Python = 3
    Java = 4
    Unknown = 999


class Solution(Base):
    __tablename__ = "solutions"
    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, index=True)
    nickname = Column(String)
    result = Column(Enum(ResultEnum))
    time_used = Column(Integer)
    memory_used = Column(Integer)
    code_len = Column(Integer)
    language = Column(Enum(LanguageEnum))
    submitted_at = Column(DateTime)

    problem_id = Column(Integer, ForeignKey("problems.id"))
    problem = relationship(Problem, backref="solutions")

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, backref="steps")
