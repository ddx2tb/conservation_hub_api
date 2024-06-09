from datetime import datetime

from pydantic import BaseModel, UUID4


class CreateEcosystemModel(BaseModel):
    name: str
    description: str
    creation_date: datetime


class EcosystemModel(CreateEcosystemModel):
    id: UUID4

    class Config:
        from_attributes = True
