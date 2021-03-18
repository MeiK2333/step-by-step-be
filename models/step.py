from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.db import Base


class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    source = Column(String)

    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", backref="steps")
