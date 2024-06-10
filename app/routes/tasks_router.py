from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import Task
from app.database import get_db
from app.schemas import TaskModel, CreateTaskModel, UserModel
from app.utils.db import get_register_by_id, get_register_by_id_or_404_exception, delete_by_id_or_404_exception
from app.utils.user import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskModel, status_code=status.HTTP_201_CREATED)
async def create(task: CreateTaskModel, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> TaskModel:
    sqla_resource: Optional[Task] = Task(
        project_id=task.project_id,
        name=task.name,
        description=task.description,
        start_date=task.start_date,
        end_date=task.end_date,
        status=task.status,
    )
    db.add(sqla_resource)
    db.commit()

    return TaskModel.from_orm(sqla_resource)


@router.get("/{task_id}", response_model=TaskModel, status_code=status.HTTP_200_OK)
async def read(task_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
               db: Annotated[Session, Depends(get_db)]) -> TaskModel:
    sqla_task: Optional[Task] = await get_register_by_id_or_404_exception(Task, task_id, db)
    return TaskModel.from_orm(sqla_task)


@router.put("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(task_id: UUID4, task: TaskModel, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    sqla_task: Optional[Task] = await get_register_by_id(db, Task, task_id)

    if not sqla_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    sqla_task.id = task.id
    sqla_task.project_id = task.project_id
    sqla_task.name = task.name
    sqla_task.description = task.description
    sqla_task.start_date = task.start_date
    sqla_task.end_date = task.end_date
    sqla_task.status = task.status

    db.commit()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    return await delete_by_id_or_404_exception(Task, task_id, db)
