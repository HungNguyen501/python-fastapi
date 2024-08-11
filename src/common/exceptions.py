"""Exceptions when handling data"""
from http import HTTPStatus

from fastapi import HTTPException


class NotFoundException(HTTPException):
    """Exception in case not found user in database"""
    def __init__(self, detail: str = "Item not found") -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail,)


class InvalidInputException(HTTPException):
    """Exception when passing invalid input data for query"""
    def __init__(self, detail: str = "Invalid input") -> None:
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail,)


class UnicornException(Exception):
    """General exception"""
    def __init__(self, value: str):
        self.value = value


class CredentialsException(HTTPException):
    """Exception in case InvalidTokenError raises """
    def __init__(self, detail: str):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )
