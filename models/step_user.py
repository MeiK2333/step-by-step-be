from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.db import Base
from models.user import User


class StepUser(Base):
    __tablename__ = "step_user"
    id = Column(Integer, primary_key=True, index=True)

    clazz = Column(String)
    nickname = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, backref="step_users")

    step_id = Column(Integer, ForeignKey("steps.id"))
    step = relationship("Step", backref="step_users")
