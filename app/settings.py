from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    title: str = "Conservation HUB"

    SECRET_KEY: str = "7c092a782a5834d281aa1bbd05544e4e905828c239e81800554c8a15e4f3fd5a"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


default_settings = Settings()
