from pydantic import BaseModel, UUID4


class CreateResourceAssignmentModel(BaseModel):
    task_id: int
    resource_id: int
    assigned_quantity: int


class ResourceAssignmentModel(CreateResourceAssignmentModel):
    id: UUID4

    class Config:
        from_attributes = True
