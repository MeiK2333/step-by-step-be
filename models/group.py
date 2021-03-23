from typing import List

from sqlalchemy import Column, Integer, String

from models.db import Base
from models.step import Step


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(length=32), unique=True)
    name = Column(String(length=64))

    steps: List["Step"]
