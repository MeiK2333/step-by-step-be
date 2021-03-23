from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from models.db import Base
from models.source import Source


class BindUser(Base):
    __tablename__ = "bind_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=64), index=True)
    link = Column(String(length=256))

    last_spider = Column(Integer, default=0)

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, backref="bind_users")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="bind_users")

    __table_args__ = (UniqueConstraint("username", "source_id"),)
