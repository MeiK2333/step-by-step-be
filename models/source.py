from sqlalchemy import Column, Integer, String

from models.db import Base


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    link = Column(String)
