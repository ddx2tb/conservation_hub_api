from pydantic import BaseModel


class CreateResourceModel(BaseModel):
    name: str
    description: str
    quantity: int


class ResourceModel(CreateResourceModel):
    id: int

    class Config:
        from_attributes = True
