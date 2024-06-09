from datetime import datetime

from pydantic import BaseModel, UUID4


class CreateTaskModel(BaseModel):
    project_id: int
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str


class TaskModel(CreateTaskModel):
    id: UUID4

    class Config:
        from_attributes = True
