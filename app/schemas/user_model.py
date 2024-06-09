from pydantic import BaseModel, UUID4


class CreateOrUpdateUserModel(BaseModel):
    username: str
    password: str


class UserModel(BaseModel):
    username: str
    id: UUID4

    class Config:
        from_attributes = True
