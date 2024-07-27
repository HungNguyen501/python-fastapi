"""Exception Handler module"""
import functools
from http import HTTPStatus

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from src.common.exceptions import UnicornException


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


def alert(alert_name, exceptions=(Exception,), suppress=False, exc=None):  # pylint: disable=unused-argument
    """ DMP alert decorator """
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as exc:
                if suppress:
                    logger.error(f"Suppressed error for {alert_name}: {exc}")
                    return exc
                raise

        return inner
    return wrapper
