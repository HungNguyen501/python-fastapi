"""Unit tests for auth_service module"""
import json
from datetime import datetime
from unittest.mock import patch, AsyncMock

import pytest
import jwt
from faker import Faker
from freezegun import freeze_time
from src.mocks import SettingsMock
from src.common.crypto import hash_password
from src.services.auth.auth_service import AuthService, get_current_user_uuid
from src.schemas.user_schema import UserCreate, UserInDB
from src.exceptions.exceptions import CredentialsException


fake = Faker()


def fake_user_record(name: str, password: str):
    """Fake user record in DB"""
    return UserInDB(
        uuid=fake.uuid4(),
        name=name,
        password=hash_password(plain_password=password)
    )


def fake_token(playload: dict):
    """Fake json web token"""
    mock_settings = SettingsMock()
    return jwt.encode(
        payload=playload,
        key=mock_settings.SECRET_KEY,
        algorithm=mock_settings.ALGORITHM
    )


@freeze_time("2000-01-01")
def fake_expired_token():
    """Fake expried json web token"""
    mock_settings = SettingsMock()
    return jwt.encode(
        payload={
            "uuid": fake.uuid4(),
            "expires_at": datetime.timestamp(datetime.now())
        },
        key=mock_settings.SECRET_KEY,
        algorithm=mock_settings.ALGORITHM
    )


@pytest.mark.asyncio
@freeze_time("2010-01-01")
@patch(target="src.services.auth.auth_service.get_settings", return_value=SettingsMock())
async def test_auth_service_class(*_):
    """Test AuthService class"""
    auth_service = AuthService(base_service=AsyncMock(), redis_pool=AsyncMock())
    # Test create_user function
    mock_data = UserCreate(name="bob", password="1")
    result = await auth_service.create_user(data=mock_data)
    assert result.message == "created"
    # Test authenticate function
    auth_service.redis_pool.get.side_effect = [
        None,
        json.dumps({"uuid": fake.uuid4()}),
        json.dumps({"uuid": fake.uuid4()})
    ]
    # In case: user_name does not exist in redis
    with pytest.raises(CredentialsException):
        await auth_service.authenticate(username="alice", password="fake_pass")
    # In case: password is wrong
    fake_name = fake.user_name()
    fake_pass = fake.password()
    auth_service.base_service.get.return_value = fake_user_record(name=fake_name, password=fake_pass)
    with pytest.raises(CredentialsException):
        await auth_service.authenticate(username=fake_name, password=fake.password())
    # Happy path
    result = await auth_service.authenticate(username=fake_name, password=fake_pass)
    assert result.token_type == "bearer"


@pytest.mark.asyncio
@freeze_time("2010-01-01")
@patch(target="src.services.auth.auth_service.get_settings", return_value=SettingsMock())
async def test_get_current_user_uuid(*_):
    """Test get_current_user_uuid function"""
    # In case: Invalid credentials
    with pytest.raises(CredentialsException) as exc:
        await get_current_user_uuid(token="invalid_token")
    assert exc.value.detail == "Invalid credentials"
    # In case: Token does not include UUID
    with pytest.raises(CredentialsException) as exc:
        await get_current_user_uuid(
            token=fake_token(playload={"dum": "foo"})
        )
    assert exc.value.detail == "Token does not include UUID"
    # In case: Toke expires
    with pytest.raises(CredentialsException) as exc:
        await get_current_user_uuid(
            token=fake_expired_token())
    assert exc.value.detail == "Token expires"
    # Happy path
    fake_uuid = fake.uuid4()
    assert fake_uuid == await get_current_user_uuid(
        token=fake_token(playload={
            "uuid": fake_uuid,
            "expires_at": datetime.timestamp(datetime.now())
        })
    )
