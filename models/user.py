from sqlalchemy import Column, Integer, String, Boolean

from models.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=64), unique=True)

    robot = Column(Boolean, default=False)
