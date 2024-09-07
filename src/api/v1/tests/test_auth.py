"""Unit test for auth module"""
from src.mocks import make_test_client


def test_login():
    """Test login API"""
    response = make_test_client().post(
        url="/api/v1/auth",
        headers={'accept': 'application/json'},
        files=[],
        data={
            'grant_type': 'password',
            'username': 'user1',
            'password': '123'
        }
    )
    assert response.text == '{"access_token":"fake_toke","token_type":"bearer"}'
    assert response.status_code == 200
