from fastapi import FastAPI
from toolz import pipe

from app.database import Base, engine
from app.routes.ecosystems_router import router as ecosystems_router
from app.routes.projects_router import router as projects_router
from app.routes.resources_assignment_router import router as resources_assignment_router
from app.routes.resources_router import router as resources_router
from app.routes.tasks_router import router as tasks_router
from app.routes.users_router import router as users_router
from app.settings import Settings

Base.metadata.create_all(bind=engine)


def register_routes(app: FastAPI) -> FastAPI:
    app.include_router(ecosystems_router)
    app.include_router(projects_router)
    app.include_router(tasks_router)
    app.include_router(resources_router)
    app.include_router(resources_assignment_router)
    app.include_router(users_router)
    return app


def create_app(project_settings: Settings) -> FastAPI:
    return FastAPI(title=project_settings.title, )


def init_app(project_settings: Settings) -> FastAPI:
    return pipe(
        project_settings,
        create_app,
        register_routes,
    )
