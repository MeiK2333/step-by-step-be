from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.db import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=64), index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="roles")
