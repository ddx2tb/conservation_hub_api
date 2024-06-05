from fastapi import FastAPI

from app.fastapi import init_app
from app.settings import Settings

settings = Settings(
    title="Conservation HUB",
)

app: FastAPI = init_app(settings)
