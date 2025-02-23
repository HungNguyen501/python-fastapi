"""Mock services"""
from fastapi.testclient import TestClient
from src.api.application import get_app
from src.services import AuthService, UserService, get_current_user_uuid
from src.services.auth.tests.mocks import mock_auth_service
from src.services.business.tests.mocks import mock_user_service
from src.common.faker import StringFaker


def make_test_client():
    """Mock FastAPI application"""
    async def fake_current_user_uuid():
        """Fake user_uuid"""
        return StringFaker.random_uuid()
    app = get_app()
    app.dependency_overrides[AuthService] = mock_auth_service
    app.dependency_overrides[UserService] = mock_user_service
    app.dependency_overrides[get_current_user_uuid] = fake_current_user_uuid
    return TestClient(app=app)
