from datetime import datetime

from pydantic import BaseModel


class CreateEcosystemModel(BaseModel):
    name: str
    description: str
    creation_date: datetime


class EcosystemModel(CreateEcosystemModel):
    id: int

    class Config:
        from_attributes = True
