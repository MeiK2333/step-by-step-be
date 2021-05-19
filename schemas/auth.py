from datetime import timedelta, datetime
from typing import Optional, List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import SECRET_KEY
from models.db import get_db
from models.user import User
from models.role import Role as RoleModel
from schemas.exception import SBSException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Auth(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    roles: List[Role] = []

    class Config:
        orm_mode = True


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_auth(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = SBSException(
        errmsg="Could not validate credentials", errcode=401
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    auth = db.query(User).filter(User.username == username).first()
    if auth is None:
        raise credentials_exception
    return auth


async def get_current_admin(auth=Depends(get_current_auth)):
    roles: List[RoleModel] = auth.roles
    for role in roles:
        if role.name == "admin":
            return auth
    raise SBSException(errmsg="无权进行此操作", errcode=403)


def create_access_token(
    user: User, expires_delta: Optional[timedelta] = None, db: Session = None
):
    to_encode = {"username": user.username}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=365)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
