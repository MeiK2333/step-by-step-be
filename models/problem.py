from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from models.db import Base
from models.source import Source


class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(String(length=128), index=True)

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, backref="problems")
    title = Column(String(length=128), default="")
    link = Column(String(length=256), default="")

    __table_args__ = (UniqueConstraint("source_id", "problem_id"),)
