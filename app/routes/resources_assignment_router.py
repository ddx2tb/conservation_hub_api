from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import ResourceAssignment
from app.database import get_db
from app.schemas import CreateResourceAssignmentModel, ResourceAssignmentModel, UserModel
from app.utils.db import get_register_by_id, get_register_by_id_or_404_exception, delete_by_id_or_404_exception
from app.utils.user import get_current_user

router = APIRouter(prefix="/resources_assignment", tags=["resources_assignment"])


@router.post("/", response_model=ResourceAssignmentModel, status_code=status.HTTP_201_CREATED)
async def create(resource_assignment: CreateResourceAssignmentModel,
                 _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> ResourceAssignmentModel:
    sqla_resource_assignment: Optional[ResourceAssignment] = ResourceAssignment(
        task_id=resource_assignment.task_id,
        resource_id=resource_assignment.resource_id,
        assigned_quantity=resource_assignment.assigned_quantity,
    )
    db.add(sqla_resource_assignment)
    db.commit()

    return ResourceAssignmentModel.from_orm(sqla_resource_assignment)


@router.get("/{resource_assignment_id}", response_model=ResourceAssignmentModel, status_code=status.HTTP_200_OK)
async def read(resource_assignment_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
               db: Annotated[Session, Depends(get_db)]) -> ResourceAssignmentModel:
    sqla_resource_assignment = await get_register_by_id_or_404_exception(ResourceAssignment, resource_assignment_id, db)
    return ResourceAssignmentModel.from_orm(sqla_resource_assignment)


@router.put("/{resource_assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(resource_assignment_id: UUID4, resource_assignment: ResourceAssignmentModel,
                 _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    sqla_resource_assignment: Optional[ResourceAssignment] = await get_register_by_id(db, ResourceAssignment,
                                                                                      resource_assignment_id)

    if not sqla_resource_assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    sqla_resource_assignment.task_id = resource_assignment.task_id
    sqla_resource_assignment.resource_id = resource_assignment.resource_id
    sqla_resource_assignment.assigned_quantity = resource_assignment.assigned_quantity

    db.commit()


@router.delete("/{resource_assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(resource_assignment_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    return await delete_by_id_or_404_exception(ResourceAssignment, resource_assignment_id, db)
