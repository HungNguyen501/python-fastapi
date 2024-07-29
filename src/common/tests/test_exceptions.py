"""Unit tests for exception module"""
from http import HTTPStatus

from fastapi import HTTPException
from src.common.exceptions import (
    NotFoundException,
    InvalidInputException,
    UnicornException,
)


def test_not_found_exception_constructor():
    """Test NotFoundException constructor"""
    exc = NotFoundException()
    assert isinstance(exc, HTTPException) is True
    assert exc.status_code == HTTPStatus.NOT_FOUND
    assert exc.detail == "Item not found"


def test_invalid_input_exception_constructor():
    """Test InvalidInputException constructor"""
    exc = InvalidInputException()
    assert isinstance(exc, HTTPException) is True
    assert exc.status_code == HTTPStatus.BAD_REQUEST
    assert exc.detail == "Invalid input"


def test_unicorn_exception_constructor():
    """Test UnicornException constructor"""
    exc = UnicornException("dummy")
    assert isinstance(exc, Exception) is True
    assert str(exc) == "dummy"
