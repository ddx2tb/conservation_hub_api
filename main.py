from fastapi import FastAPI

from app.fastapi import init_app
from app.settings import default_settings

app: FastAPI = init_app(default_settings)
