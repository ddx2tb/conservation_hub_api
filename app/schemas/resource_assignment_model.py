from pydantic import BaseModel


class CreateResourceAssignmentModel(BaseModel):
    task_id: int
    resource_id: int
    assigned_quantity: int


class ResourceAssignmentModel(CreateResourceAssignmentModel):
    id: int

    class Config:
        from_attributes = True
