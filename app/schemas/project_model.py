from datetime import datetime

from pydantic import BaseModel, UUID4


class CreateProjectModel(BaseModel):
    name: str
    description: str
    ecosystem_id: int
    creation_date: datetime
    modification_date: datetime


class ProjectModel(CreateProjectModel):
    id: UUID4

    class Config:
        from_attributes = True
