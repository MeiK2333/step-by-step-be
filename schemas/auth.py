from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import SECRET_KEY
from models.db import get_db
from models.user import User as AuthModel
from schemas.exception import SBSException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth(BaseModel):
    id: int
    username: str
    email: str
    nickname: Optional[str] = None


async def get_current_auth(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = SBSException(errmsg="Could not validate credentials", errcode=401)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    auth = db.query(AuthModel).filter(AuthModel.email == email).first()
    if auth is None:
        raise credentials_exception
    return auth


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None, db: Session = None
):
    to_encode = {"email": data.get("email")}
    email: str = to_encode.get("email")
    user = db.query(AuthModel).filter(AuthModel.email == email).first()
    if user is None:
        # 因为此处的数据是从 GitHub 获取而非用户提交，因此可以信任，直接创建入库
        db_user = AuthModel(
            username=data.get("login"),
            email=data.get("email"),
            nickname=data.get("name"),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
