from datetime import datetime

from pydantic import BaseModel


class CreateProjectModel(BaseModel):
    ecosystem_id: int
    creation_date: datetime
    modification_date: datetime


class ProjectModel(CreateProjectModel):
    id: int

    class Config:
        from_attributes = True
