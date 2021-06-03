from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship

from models.db import Base
from models.source import Source


def bind_user_link(content):
    engine = content.engine
    query = engine.execute(
        text("select * from sources where id = :source_id"),
        {"source_id": content.get_current_parameters()["source_id"]},
    )
    name = ""
    for cur in query:
        name = cur.name
    username = content.get_current_parameters()["username"]
    if name == "SDUT":
        return f"https://acm.sdut.edu.cn/onlinejudge3/users?username={username}"
    elif name == "POJ":
        return f"http://poj.org/userstatus?user_id={username}"
    elif name == "VJ":
        return f"https://vjudge.net/user/{username}"
    elif name == "CF":
        return f"https://codeforces.com/profile/{username}"
    return ""


class BindUser(Base):
    __tablename__ = "bind_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=64), index=True)
    link = Column(String(length=256), default=bind_user_link)

    last_spider = Column(Integer, default=0)

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, backref="bind_users")

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="bind_users")

    __table_args__ = (UniqueConstraint("username", "source_id"),)
