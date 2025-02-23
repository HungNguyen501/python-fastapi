"""Unit test for auth module"""
from src.api.tests.mocks.test_client import make_test_client
from src.common.faker import StringFaker


def test_login():
    """Test login API"""
    response = make_test_client().post(
        url="/api/v1/auth",
        headers={'accept': 'application/json'},
        files=[],
        data={
            "grant_type": "password",
            "username": StringFaker.random_name(),
            "password": StringFaker.random_password()
        }
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None
