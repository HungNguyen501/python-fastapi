"""API application"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from src.api.v1.router import get_api_router
from src.common.exception_handler import http_exception_handler, unicorn_exception_handler
from src.db.database import DatabaseSessionManager


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
    """Define startup and shutdown logics in lifetime of application"""
    session_manager = DatabaseSessionManager()
    yield
    await session_manager.close()


def get_app():
    """Get FastAPI application"""
    app = FastAPI(
        title="API service",
        lifespan=lifespan,
        exception_handlers={
            Exception: unicorn_exception_handler,
            HTTPException: http_exception_handler,
        }
    )
    app.include_router(router=get_api_router(), prefix="/api")
    return app
