"""Unit tests for user model"""
import json

from src.mocks import make_test_client


def test_get_user():
    """Test get_user"""
    response = make_test_client().get(
        url="/api/v1/user/",
        headers={
            "Authorization": "Bearer fake_token",
            "Accept": "application/json"
        },
    )
    assert response.status_code == 200
    assert response.json()["uuid"] is not None
    assert response.json()["name"] is not None
    assert response.json()["password"] is not None


def test_create_user():
    """Test create_user"""
    response = make_test_client().post(
        url="/api/v1/user",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "name": "bob",
            "password": "123"
        })
    )
    assert response.status_code == 200
    assert response.text == '{"message":"created"}'


def test_update_user():
    """Test update_user"""
    response = make_test_client().put(
        url="/api/v1/user",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "password": "123"
        })
    )
    assert response.status_code == 200
    assert response.text == '{"message":"updated"}'


def test_delete_user():
    """Test delete_user"""
    response = make_test_client().delete(
        url="/api/v1/user/",
        headers={
            "Authorization": "Bearer fake_token",
            "Accept": "application/json"
        },
    )
    assert response.status_code == 200
    assert response.text == '{"message":"deleted"}'


def test_list_user():
    """Test list_users"""
    response = make_test_client().get(
        url="/api/v1/user/list?start=0&page_size=10"
    )
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["count"] == 1
    assert len(response.json()["users"]) == 1
