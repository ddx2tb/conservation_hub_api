from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import Ecosystem
from app.database import get_db
from app.schemas import CreateEcosystemModel, EcosystemModel, UserModel
from app.utils.db import get_register_by_id_or_404_exception, delete_by_id_or_404_exception
from app.utils.user import get_current_user

router = APIRouter(prefix="/ecosystems", tags=["ecosystems"])


@router.post("/", response_model=EcosystemModel, status_code=status.HTTP_201_CREATED)
async def create(ecosystem: CreateEcosystemModel, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> EcosystemModel:
    sqla_ecosystem: Optional[Ecosystem] = Ecosystem(
        name=ecosystem.name,
        description=ecosystem.description,
    )
    db.add(sqla_ecosystem)
    db.commit()

    return EcosystemModel.from_orm(sqla_ecosystem)


@router.get("/{ecosystem_id}", response_model=EcosystemModel, status_code=status.HTTP_200_OK)
async def read(ecosystem_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
               db: Annotated[Session, Depends(get_db)]) -> EcosystemModel:
    sqla_ecosystem: Optional[Ecosystem] = await get_register_by_id_or_404_exception(Ecosystem, ecosystem_id, db)
    return EcosystemModel.from_orm(sqla_ecosystem)


@router.put("/{ecosystem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(ecosystem_id: UUID4, ecosystem: EcosystemModel,
                 _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    sqla_ecosystem: Optional[Ecosystem] = await get_register_by_id_or_404_exception(Ecosystem, ecosystem_id, db)

    if not sqla_ecosystem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    sqla_ecosystem.id = ecosystem.id
    sqla_ecosystem.name = ecosystem.name
    sqla_ecosystem.description = ecosystem.description
    sqla_ecosystem.creation_date = ecosystem.creation_date

    db.commit()


@router.delete("/{ecosystem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(ecosystem_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    return await delete_by_id_or_404_exception(Ecosystem, ecosystem_id, db)
