"""API application"""
from fastapi import FastAPI
from src.api.v1.router import api_router

from src.common.exception_handler import http_exception_handler, unicorn_exception_handler, HTTPException


def get_app():
    """Get FastAPI application"""
    app = FastAPI(
        title="API service",
        exception_handlers={
            Exception: unicorn_exception_handler,
            HTTPException: http_exception_handler,
        }
    )
    app.include_router(router=api_router, prefix="/api")
    return app
