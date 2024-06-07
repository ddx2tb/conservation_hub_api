from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import Resource
from app.database import get_db
from app.schemas import CreateResourceModel, ResourceModel
from app.utils.db import get_register_by_id, get_register_by_id_or_404_exception, delete_by_id_or_404_exception

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("/", response_model=ResourceModel, status_code=HTTPStatus.CREATED)
async def create(resource: CreateResourceModel, db: Session = Depends(get_db)) -> ResourceModel:
    sqla_resource: Optional[Resource] = Resource(
        name=resource.name,
        description=resource.description,
        quantity=resource.quantity,
    )
    db.add(sqla_resource)
    db.commit()

    return ResourceModel.from_orm(sqla_resource)


@router.get("/{resource_id}", response_model=ResourceModel, status_code=HTTPStatus.OK)
async def read(resource_id: int, db: Session = Depends(get_db)) -> ResourceModel:
    sqla_resource: Optional[Resource] = await get_register_by_id_or_404_exception(Resource, resource_id, db)
    return ResourceModel.from_orm(sqla_resource)


@router.put("/{resource_id}", status_code=HTTPStatus.NO_CONTENT)
async def update(resource_id: int, resource: ResourceModel, db: Session = Depends(get_db)) -> None:
    sqla_resource: Optional[Resource] = await get_register_by_id(db, Resource, resource_id)

    if not sqla_resource:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    sqla_resource.name = resource.name
    sqla_resource.description = resource.description
    sqla_resource.quantity = resource.quantity

    db.commit()


@router.delete("{resource_id}/", status_code=HTTPStatus.NO_CONTENT)
async def delete(resource_id: int, db: Session = Depends(get_db)) -> None:
    return await delete_by_id_or_404_exception(Resource, resource_id, db)
