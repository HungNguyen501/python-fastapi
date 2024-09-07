"""Unit tests for hehealh_check module"""
from fastapi.testclient import TestClient
from src.api.application import get_app


app = get_app()
test_client = TestClient(app=app)


def test_get_health_check(*_):
    """Test health_check API"""
    response = test_client.get(url="/api/v1/health")
    assert response.status_code == 200
    assert response.text == '{"message":"200 OK"}'
