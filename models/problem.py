from sqlalchemy import Column, Integer, String

from models.db import Base


class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(String)
    source = Column(String)
    title = Column(String, default="")
    link = Column(String, default="")
