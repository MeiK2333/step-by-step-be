from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session, Session

from config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base:
    __allow_unmapped__ = True

Base = declarative_base(cls=Base)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
