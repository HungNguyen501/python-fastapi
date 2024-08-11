"""Unit test for auth module"""
from unittest.mock import AsyncMock, MagicMock

import pytest
from src.api.v1.auth import login


@pytest.mark.asyncio
async def test_login():
    """Test login function"""
    mock_auth_service = AsyncMock()
    mock_credentials = MagicMock()
    mock_credentials.username = "bob"
    mock_credentials.password = "-1"
    mock_auth_service.authenticate.return_value = 1
    assert await login(user_credentials=mock_credentials, auth_service=mock_auth_service) == 1
