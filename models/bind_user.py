from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.db import Base
from models.source import Source


class BindUser(Base):
    __tablename__ = "bind_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    link = Column(String)

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, backref="bind_users")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="bind_users")
