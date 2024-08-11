"""Unit tests for auth_service module"""
import json
from unittest.mock import patch, AsyncMock

from freezegun import freeze_time
import pytest
from src.services.auth_service import AuthService, get_current_user_uuid
from src.schemas.user_schema import UserCreate, UserInDB
from src.common.exceptions import CredentialsException


@pytest.mark.asyncio
@freeze_time("2024-01-01")
@patch(target="src.db.database.get_settings")
async def test_auth_service_class(mock_settings):
    """Test AuthService class"""
    mock_user_service = AsyncMock()
    mock_redis_pool = AsyncMock()
    auth_service = AuthService(mock_user_service, mock_redis_pool)
    # Test creat_user function
    mock_data = UserCreate(name="bob", password="1")
    result = await auth_service.create_user(data=mock_data)
    assert result.message == "created"
    # Test authenticate function
    mock_settings.return_value.SECRET_KEY.__str__.return_value = "dum_key"
    mock_settings.return_value.ALGORITHM.__str__.return_value = "HS256"
    auth_service.redis_pool.get.side_effect = [None, json.dumps({"uuid": "-1"}), json.dumps({"uuid": "-1"})]
    with pytest.raises(CredentialsException):
        await auth_service.authenticate(username="bob", password="-1")
    mock_user_data = UserInDB(uuid="a00a0aaa-0aa0-00a0-00aa-0a0aa0aa00a0", name="bob", password="$2b$12$eeeeeeeeeeeeeeeeeeeeeeVNjYkVPE40j7qKCyXsS6ba1VUVbOLKO")  # noqa: E501 # pylint: disable=line-too-long
    auth_service.user_service.get.return_value = mock_user_data
    # In case: password is wrong
    with pytest.raises(CredentialsException):
        await auth_service.authenticate(username="bob", password="0")
    result = await auth_service.authenticate(username="bob", password="-1")
    assert result.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiLTEiLCJleHBpcmVzX2F0IjoxNzA0MDY3NTAwLjB9.2H6JFMDS3E7UME5nmhtTc07BruyTxqY5508TVWQlwjk"  # noqa: E501 # pylint: disable=line-too-long
    assert result.token_type == "bearer"


@pytest.mark.asyncio
@freeze_time("2024-01-02")
@patch(target="src.db.database.get_settings")
async def test_get_current_user_uuid(mock_settings):
    """Test get_current_user_uuid function"""
    # In case: Invalid credentials
    with pytest.raises(CredentialsException) as exc:
        await get_current_user_uuid(token="-1")
    assert exc.value.detail == "Invalid credentials"
    # In case: UUID is null
    mock_settings.return_value.SECRET_KEY.__str__.return_value = "dum_key"
    mock_settings.return_value.ALGORITHM.__str__.return_value = "HS256"
    with pytest.raises(CredentialsException) as exc:
        await get_current_user_uuid(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhYmMiOiItMSIsImV4cGlyZXNfYXQiOjE3MDQwNjc1MDAuMH0.xtZqOyPMRXfbrSy3Nym64kJ0HHK3PO97EHyFULvdMUY")  # noqa: E501 # pylint: disable=line-too-long
    assert exc.value.detail == "Token does not include UUID"
    # In case: Toke expires
    with pytest.raises(CredentialsException) as exc:
        await get_current_user_uuid(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiLTEiLCJleHBpcmVzX2F0IjoxNzA0MDY3NTAwLjB9.2H6JFMDS3E7UME5nmhtTc07BruyTxqY5508TVWQlwjk")  # noqa: E501 # pylint: disable=line-too-long
    assert exc.value.detail == "Token expires"
    # In case: successful
    assert "-1" == await get_current_user_uuid(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiLTEiLCJleHBpcmVzX2F0IjoxNzA0MTUzOTAwLjB9.ZL2Y8zc0xpG43NI4tLsDKC9okKtUYtAbfR7rq2jgd9w")  # noqa: E501 # pylint: disable=line-too-long
