"""Mock services"""
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from faker import Faker
from src.api.application import get_app
from src.schemas.auth_schema import TokenSchema
from src.services import AuthService, UserService, get_current_user_uuid


fake = Faker()


async def mock_auth_service():
    """Mock AuthService object"""
    mock_auth = AsyncMock()
    mock_auth.authenticate.return_value = TokenSchema(
        access_token="fake_toke",
        token_type="bearer"
    )
    mock_auth.create_user.return_value = {"message": "created"}
    return mock_auth


async def mock_user_service():
    """Mock UserService object"""
    mock_us = AsyncMock()
    mock_us.get.return_value = {
        "uuid": fake.uuid4(),
        "name": fake.user_name(),
        "password": fake.password(),
    }
    mock_us.update.return_value = {"message": "updated"}
    mock_us.delete.return_value = {"message": "deleted"}
    mock_us.list_users.return_value = {
        "total": 1,
        "count": 1,
        "users": [
            {"name": fake.user_name()}
        ]
    }
    return mock_us


async def fake_current_user_uuid():
    """Fake user_uuid"""
    return fake.uuid4()


def make_test_client():
    """Mock FastAPI application"""
    app = get_app()
    app.dependency_overrides[AuthService] = mock_auth_service
    app.dependency_overrides[UserService] = mock_user_service
    app.dependency_overrides[get_current_user_uuid] = fake_current_user_uuid
    return TestClient(app=app)
