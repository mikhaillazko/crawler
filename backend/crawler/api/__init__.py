from fastapi import FastAPI

from .link_api import router as link_router
from .task_api import router as task_router

__all__ = (
    "register_routers",
)


def register_routers(app: FastAPI, prefix: str):
    app.include_router(task_router, prefix=prefix)
    app.include_router(link_router, prefix=prefix)
