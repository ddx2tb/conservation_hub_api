from pydantic import BaseModel, UUID4


class CreateResourceModel(BaseModel):
    name: str
    description: str
    quantity: int


class ResourceModel(CreateResourceModel):
    id: UUID4

    class Config:
        from_attributes = True
