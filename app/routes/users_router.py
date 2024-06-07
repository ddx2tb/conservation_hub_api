from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserModel, CreateOrUpdateUserModel
from app.utils.db import get_register_by_id, get_register_by_id_or_404_exception, delete_by_id_or_404_exception

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserModel, status_code=HTTPStatus.CREATED)
async def create(user: CreateOrUpdateUserModel, db: Session = Depends(get_db)) -> UserModel:
    sqla_resource: Optional[User] = User(
        username=user.username,
        password=user.password,
    )
    db.add(sqla_resource)
    db.commit()

    return UserModel.from_orm(sqla_resource)


@router.get("/{user_id}", response_model=UserModel, status_code=HTTPStatus.OK)
async def read(user_id: int, db: Session = Depends(get_db)) -> UserModel:
    sqla_user: Optional[User] = await get_register_by_id_or_404_exception(User, user_id, db)
    return UserModel.from_orm(sqla_user)


@router.put("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def update(user_id: int, user: CreateOrUpdateUserModel, db: Session = Depends(get_db)) -> None:
    sqla_user: Optional[User] = await get_register_by_id(db, User, user_id)

    if not sqla_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    sqla_user.username = user.username
    sqla_user.password = user.password

    db.commit()


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete(user_id: int, db: Session = Depends(get_db)) -> None:
    return await delete_by_id_or_404_exception(User, user_id, db)
