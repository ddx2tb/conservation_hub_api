from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import Ecosystem
from app.database import get_db
from app.schemas import CreateEcosystemModel, EcosystemModel
from app.utils.db import get_register_by_id_or_404_exception, delete_by_id_or_404_exception

router = APIRouter(prefix="/ecosystems", tags=["ecosystems"])


@router.post("/", response_model=EcosystemModel, status_code=HTTPStatus.CREATED)
async def create(ecosystem: CreateEcosystemModel, db: Session = Depends(get_db)) -> EcosystemModel:
    sqla_ecosystem: Optional[Ecosystem] = Ecosystem(
        name=ecosystem.name,
        description=ecosystem.description,
    )
    db.add(sqla_ecosystem)
    db.commit()

    return EcosystemModel.from_orm(sqla_ecosystem)


@router.get("/{ecosystem_id}", response_model=EcosystemModel, status_code=HTTPStatus.OK)
async def read(ecosystem_id: int, db: Session = Depends(get_db)) -> EcosystemModel:
    sqla_ecosystem = await get_register_by_id_or_404_exception(Ecosystem, ecosystem_id, db)
    return EcosystemModel.from_orm(sqla_ecosystem)


@router.put("/{ecosystem_id}", status_code=HTTPStatus.NO_CONTENT)
async def update(ecosystem_id: int, ecosystem: EcosystemModel, db: Session = Depends(get_db)) -> None:
    sqla_ecosystem: Optional[Ecosystem] = db.query(Ecosystem).filter(Ecosystem.id == ecosystem_id).first()

    if not sqla_ecosystem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    sqla_ecosystem.id = ecosystem.id
    sqla_ecosystem.name = ecosystem.name
    sqla_ecosystem.description = ecosystem.description
    sqla_ecosystem.creation_date = ecosystem.creation_date

    db.commit()


@router.delete("/{ecosystem_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete(ecosystem_id: int, db: Session = Depends(get_db)) -> None:
    return await delete_by_id_or_404_exception(Ecosystem, ecosystem_id, db)
