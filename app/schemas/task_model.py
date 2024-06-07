from datetime import datetime

from pydantic import BaseModel


class CreateTaskModel(BaseModel):
    project_id: int
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str


class TaskModel(CreateTaskModel):
    id: int

    class Config:
        from_attributes = True
