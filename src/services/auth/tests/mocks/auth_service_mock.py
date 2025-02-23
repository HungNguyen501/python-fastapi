"""Mock auth service"""
from unittest.mock import AsyncMock

from src.schemas.auth_schema import TokenSchema
from src.common.faker import StringFaker


async def mock_auth_service():
    """Mock AuthService object"""
    mock_auth = AsyncMock()
    mock_auth.authenticate.return_value = TokenSchema(
        access_token=StringFaker.random_token(),
        token_type="bearer"
    )
    mock_auth.create_user.return_value = {"message": "created"}
    return mock_auth
