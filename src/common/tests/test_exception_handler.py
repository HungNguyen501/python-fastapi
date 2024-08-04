"""Unit tests for exception_handler module"""
from http import HTTPStatus
from unittest.mock import call, patch, MagicMock

import pytest
from fastapi import HTTPException
from src.common.exception_handler import (
    http_exception_handler,
    unicorn_exception_handler,
    pegasus,
)


@pytest.mark.asyncio
@patch(target="src.common.exception_handler.JSONResponse")
async def test_http_exception_handler(mock_resp):
    """Test function http_exception_handler"""
    mock_exc = MagicMock()
    mock_exc.status_code = -1
    mock_exc.detail = "null"
    _ = await http_exception_handler(None, mock_exc)
    assert mock_resp.call_args == call(status_code=-1, content={'error': 'null'})


@pytest.mark.asyncio
@patch(target="src.common.exception_handler.JSONResponse")
async def test_unicorn_exception_handler(mock_resp):
    """Test function unicorn_exception_handler"""
    _ = await unicorn_exception_handler(None, "none")
    assert mock_resp.call_args == call(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={'error': 'none'})


@pytest.mark.asyncio
async def test_pegasus():
    """Test pegasus function"""
    @pegasus(target="sick",)
    async def mock_func_with_suppress():
        raise ValueError("nevermind")

    @pegasus(target="sick", allow_errors=(ValueError,),)
    async def mock_func():
        raise ValueError("fever")
    with pytest.raises(HTTPException) as exc:
        assert await mock_func_with_suppress() == HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="nevermind",
        )
    with pytest.raises(ValueError) as exc:
        await mock_func()
    assert str(exc.value) == "fever"
