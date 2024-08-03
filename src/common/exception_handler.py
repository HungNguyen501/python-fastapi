"""Exception Handler module"""
import functools
from http import HTTPStatus
import traceback

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


def pegasus(error_name: str, exceptions=(Exception,), suppress_error: bool = True):
    """Customize exception handling by:
    - Control output log in console
    - Send alert to Email/ Slack Channel
    - Return intentional response

    Args:
        error_name(str): title for exception/ error
        exceptions(tuple): list of exceptions for suppression
        suppress_error(boolean): intend to suppress exception
    """
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions:
                logger.error(f"Suppressed {error_name} error: {traceback.format_exc()}")
                # Could send error traceback to Slack channel here
                if suppress_error:
                    return
                raise
        return inner
    return wrapper
