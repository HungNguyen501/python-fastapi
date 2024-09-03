"""Exception Handler module"""
import functools
from http import HTTPStatus
import traceback

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from src.exceptions.exceptions import UnicornException


async def http_exception_handler(request: Request, exc: HTTPException):  # pylint: disable=unused-argument
    """Handle http exception"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


async def unicorn_exception_handler(request: Request, exc: UnicornException):  # pylint: disable=unused-argument
    """Handler general exception"""
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"error": str(exc)},
    )


def pegasus(target: str, allow_errors=()):
    """Customize exception handling by:
    - Control log in console
    - Send alert to Email/ Slack Channel
    - Suppress errors for handy customization

    Args:
        target(str): title for exception/ error
        allow_errors(tuple): list of expected exceptions that intends to raise
    """
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                logger.error(f"Suppressed {target} error: {traceback.format_exc()}")
                # Could send error traceback to Slack channel here
                if isinstance(exc, allow_errors):
                    raise
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail=str(exc),
                ) from exc
        return inner
    return wrapper
