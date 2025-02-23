"""Mock user service"""
from unittest.mock import AsyncMock

from src.common.faker import StringFaker


async def mock_user_service():
    """Mock UserService object"""
    mock_us = AsyncMock()
    mock_us.get.return_value = {
        "uuid": StringFaker.random_uuid(),
        "name": StringFaker.random_name(),
        "password": StringFaker.random_password(),
    }
    mock_us.update.return_value = {"message": "updated"}
    mock_us.delete.return_value = {"message": "deleted"}
    mock_us.list_users.return_value = {
        "total": 1,
        "count": 1,
        "users": [
            {"name": StringFaker.random_name()}
        ]
    }
    return mock_us
