from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.db import Base
from models.user import User


class StepUser(Base):
    __tablename__ = "step_user"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, backref="steps")

    step_id = Column(Integer, ForeignKey("steps.id"))
    step = relationship("Step", backref="users")
