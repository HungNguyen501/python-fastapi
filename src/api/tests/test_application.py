"""Unit tests for application module"""
from unittest.mock import patch, call
import sys

import pytest
from fastapi import HTTPException
from src.api.application import get_app


@patch(target="src.api.application.get_api_router")
@patch(target="src.api.application.http_exception_handler")
@patch(target="src.api.application.unicorn_exception_handler")
@patch(target="src.api.application.FastAPI")
def test_get_app(mock_fast_api, mock_unicorn_exception_handler, mock_http_exception_handler, mock_get_api_router):
    """Test get_app function"""
    mock_app = get_app()
    assert mock_fast_api.call_args == call(
        title="API service",
        exception_handlers={
            Exception: mock_unicorn_exception_handler,
            HTTPException: mock_http_exception_handler,
        })
    # pylint: disable=no-member
    assert mock_app.include_router.call_args == call(
            router=mock_get_api_router(),
            prefix="/api"
        )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__] + sys.argv[1:]))
