from typing import Optional, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserModel
from app.settings import default_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


async def get_user_by_username(username, db: Session) -> Optional[User]:
    sqla_user: Optional[User] = db.query(User).filter(
        User.username == username).first()
    return sqla_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    user: Optional[User] = await get_user_by_username(username, db)

    if not user or not verify_password(password, user.password):
        return None

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Annotated[Session, Depends(get_db)]) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, default_settings.SECRET_KEY, algorithms=[default_settings.ALGORITHM])
        username: str = payload["sub"]
    except (InvalidTokenError, KeyError):
        raise credentials_exception

    sqla_user = await get_user_by_username(username, db)

    if sqla_user is None:
        raise credentials_exception

    return UserModel.from_orm(sqla_user)
