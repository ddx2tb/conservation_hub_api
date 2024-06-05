from datetime import datetime

from pydantic import BaseModel


class CreateOrUpdateUserModel(BaseModel):
    username: str
    password: str


class UserModel(BaseModel):
    username: str

    class Config:
        from_attributes = True
