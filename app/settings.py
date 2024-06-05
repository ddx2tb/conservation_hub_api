from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    title: str
