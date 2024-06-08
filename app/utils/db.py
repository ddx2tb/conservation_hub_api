from typing import Optional, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


async def get_register_by_id(db, model, register_id) -> Optional[Any]:
    sqla_register: Optional[Any] = db.query(model).filter(
        model.id == register_id).first()
    return sqla_register


async def get_register_by_id_or_404_exception(model, register_id: int, db: Session) -> Any:
    sqla_register: Optional[Any] = await get_register_by_id(db, model, register_id)

    if not sqla_register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return sqla_register


async def delete_by_id_or_404_exception(model, register_id: int, db: Session):
    sqla_register: Optional[Any] = await get_register_by_id(db, model, register_id)

    if not sqla_register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(sqla_register)
    db.commit()
