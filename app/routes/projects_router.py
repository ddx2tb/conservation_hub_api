from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import Project
from app.database import get_db
from app.schemas import CreateProjectModel, ProjectModel
from app.utils.db import get_register_by_id, get_register_by_id_or_404_exception, delete_by_id_or_404_exception

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectModel, status_code=HTTPStatus.CREATED)
async def create(project: CreateProjectModel, db: Session = Depends(get_db)) -> ProjectModel:
    sqla_project: Optional[Project] = Project(
        ecosystem_id=project.ecosystem_id,
    )
    db.add(sqla_project)
    db.commit()

    return ProjectModel.from_orm(sqla_project)


@router.get("/{project_id}", response_model=ProjectModel, status_code=HTTPStatus.OK)
async def read(project_id: int, db: Session = Depends(get_db)) -> ProjectModel:
    sqla_project = await get_register_by_id_or_404_exception(Project, project_id, db)
    return ProjectModel.from_orm(sqla_project)


@router.put("/{project_id}", status_code=HTTPStatus.NO_CONTENT)
async def update(project_id: int, project: ProjectModel, db: Session = Depends(get_db)) -> None:
    sqla_project: Optional[Project] = await get_register_by_id(db, Project, project_id)

    if not sqla_project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    sqla_project.id = project.id
    sqla_project.ecosystem_id = project.ecosystem_id

    db.commit()


@router.delete("/{project_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete(project_id: int, db: Session = Depends(get_db)) -> None:
    return await delete_by_id_or_404_exception(Project, project_id, db)
