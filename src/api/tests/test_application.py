"""Unit tests for application module"""
from unittest.mock import patch, call, AsyncMock, MagicMock
import sys

import pytest
from fastapi import HTTPException
from src.api.application import get_app, lifespan


@pytest.mark.asyncio
@patch(target="src.api.application.DatabaseSessionManager", return_value=MagicMock())
async def test_lifespan(mock_session_manager):
    """Test lifespan function"""
    mock_session_manager.return_value.close.side_effect = AsyncMock()
    async with lifespan(None) as temp:
        _ = temp
    assert mock_session_manager.mock_calls == [call()]


@patch(target="src.api.application.lifespan")
@patch(target="src.api.application.get_api_router")
@patch(target="src.api.application.http_exception_handler")
@patch(target="src.api.application.unicorn_exception_handler")
@patch(target="src.api.application.FastAPI")
def test_get_app(mock_fastapi, mock_unicorn_exception_handler,
                 mock_http_exception_handler, mock_get_api_router, mock_lifespan, *_):
    """Test get_app function"""
    mock_app = get_app()
    assert mock_fastapi.call_args == call(
        title="API service",
        lifespan=mock_lifespan,
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
