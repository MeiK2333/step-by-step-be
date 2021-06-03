from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.db import Base


class CFRating(Base):
    __tablename__ = "cf_ratings"
    id = Column(Integer, primary_key=True, index=True)

    contest_id = Column(Integer)
    contest_name = Column(String(length=64))
    handle = Column(String(length=64))
    new_rating = Column(Integer)
    old_rating = Column(Integer)
    rank = Column(Integer)
    rating_update_time_seconds = Column(Integer)

    bind_user_id = Column(Integer, ForeignKey("bind_user.id"))
    bind_user = relationship("BindUser", backref="solutions")
