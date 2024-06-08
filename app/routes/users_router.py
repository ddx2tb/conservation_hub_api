from datetime import timedelta
from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserModel, CreateOrUpdateUserModel
from app.schemas.jwt_token_schema import JWTToken
from app.settings import default_settings
from app.utils.db import get_register_by_id, get_register_by_id_or_404_exception, delete_by_id_or_404_exception
from app.utils.jwt import create_access_token
from app.utils.user import get_user_by_username, pwd_context, authenticate_user, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create(user: CreateOrUpdateUserModel, db: Annotated[Session, Depends(get_db)]) -> UserModel:
    sqla_user: Optional[User] = await get_user_by_username(user.username, db)

    if sqla_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    sqla_resource: Optional[User] = User(
        username=user.username,
        password=pwd_context.hash(user.password),
    )
    db.add(sqla_resource)
    db.commit()

    return UserModel.from_orm(sqla_resource)


@router.get("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
async def read(user_id: int, _: Annotated[UserModel, Depends(get_current_user), None],
               db: Annotated[Session, Depends(get_db)]) -> UserModel:
    sqla_user: Optional[User] = await get_register_by_id_or_404_exception(User, user_id, db)
    return UserModel.from_orm(sqla_user)


@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(user_id: int, user: CreateOrUpdateUserModel, _: Annotated[UserModel, Depends(get_current_user), None],
               db: Annotated[Session, Depends(get_db)]) -> None:
    sqla_user: Optional[User] = await get_register_by_id(db, User, user_id)

    if not sqla_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    sqla_user.username = user.username
    sqla_user.password = user.password

    db.commit()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: int, _: Annotated[UserModel, Depends(get_current_user), None],
               db: Annotated[Session, Depends(get_db)]) -> None:
    return await delete_by_id_or_404_exception(User, user_id, db)


# JWT
@router.post("/token", response_model=JWTToken)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
) -> JWTToken:
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=default_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return JWTToken(access_token=access_token, token_type="bearer")
