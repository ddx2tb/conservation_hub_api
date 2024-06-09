from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import Project
from app.database import get_db
from app.schemas import CreateProjectModel, ProjectModel, UserModel
from app.utils.db import get_register_by_id, get_register_by_id_or_404_exception, delete_by_id_or_404_exception
from app.utils.user import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectModel, status_code=status.HTTP_201_CREATED)
async def create(project: CreateProjectModel, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> ProjectModel:
    sqla_project: Optional[Project] = Project(
        ecosystem_id=project.ecosystem_id,
        name=project.name,
    )
    db.add(sqla_project)
    db.commit()

    return ProjectModel.from_orm(sqla_project)


@router.get("/{project_id}", response_model=ProjectModel, status_code=status.HTTP_200_OK)
async def read(project_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
               db: Annotated[Session, Depends(get_db)]) -> ProjectModel:
    sqla_project: Optional[Project] = await get_register_by_id_or_404_exception(Project, project_id, db)
    return ProjectModel.from_orm(sqla_project)


@router.put("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(project_id: UUID4, project: ProjectModel, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    sqla_project: Optional[Project] = await get_register_by_id(db, Project, project_id)

    if not sqla_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    sqla_project.id = project.id
    sqla_project.ecosystem_id = project.ecosystem_id
    sqla_project.name = project.name
    sqla_project.description = project.description

    db.commit()


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(project_id: UUID4, _: Annotated[UserModel, Depends(get_current_user), None],
                 db: Annotated[Session, Depends(get_db)]) -> None:
    return await delete_by_id_or_404_exception(Project, project_id, db)
