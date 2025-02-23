"""Integration tests for user api"""
import httpx
import pytest
from src.infrastructures.databases import DatabaseConnection
from src.common.faker import StringFaker


@pytest.mark.integration_test
@pytest.fixture(name="client", scope="session")
def gen_client():
    """Mock api client"""
    with httpx.Client() as client:
        yield client


@pytest.mark.integration_test
@pytest.fixture(name="db", scope="session")
def gen_db():
    """Mock database connection"""
    with DatabaseConnection() as db:
        yield db


@pytest.mark.integration_test
def test_user_apis(client, db):
    """Test create, login, get, update, delete user apis"""
    db.truncate_table(name="users")

    username = StringFaker.random_name()
    password = StringFaker.random_password()
    # Create user
    create_response = client.post(
        url="http://127.0.0.1:8009/api/v1/user",
        headers={"Content-Type": "application/json"},
        json={
            "name": username,
            "password": password
        }
    )
    assert create_response.status_code == 200
    assert create_response.json() == {"message": "created"}
    # Login to get access token
    login_response = client.post(
        url="http://127.0.0.1:8009/api/v1/auth",
        headers={"accept": "application/json"},
        data={
            "grant_type": "password",
            "username": username,
            "password": password
        }
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    assert access_token is not None
    # Get user
    get_response = client.get(
        url="http://127.0.0.1:8009/api/v1/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
    )
    assert get_response.status_code == 200
    assert get_response.json()["name"] == username
    assert get_response.json()["password"] is not None
    assert get_response.json()["uuid"] is not None
    # Update user password
    update_response = client.put(
        url="http://127.0.0.1:8009/api/v1/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={"password": StringFaker.random_password()}
    )
    assert update_response.status_code == 200
    assert update_response.json() == {"message": "updated"}

    update_response = client.delete(
        url="http://127.0.0.1:8009/api/v1/user",
        headers={
            "Authorization": f"Bearer {access_token}",
        }
    )
    assert update_response.status_code == 200
    assert update_response.json() == {"message": "deleted"}
    db.truncate_table(name="users")


@pytest.mark.integration_test
def test_invalid_credentials(client):
    """Test login api with invalid credentials"""
    response = client.post(
        url="http://127.0.0.1:8009/api/v1/auth",
        headers={"accept": "application/json"},
        data={
            "grant_type": "password",
            "username": StringFaker.random_name(),
            "password": StringFaker.random_password()
        }
    )
    assert response.status_code == 401
    assert response.json() == {"error": "Incorrect username or password"}


@pytest.mark.integration_test
def test_list_user(client, db):
    """Test user list api"""
    db.truncate_table(name="users")
    user_number = 5

    for _ in range(user_number):
        create_response = client.post(
            url="http://127.0.0.1:8009/api/v1/user",
            headers={"Content-Type": "application/json"},
            json={
                "name": StringFaker.random_name(),
                "password": StringFaker.random_password()
            }
        )
        assert create_response.status_code == 200
        assert create_response.json() == {"message": "created"}

    response = client.get(
        url="http://127.0.0.1:8009/api/v1/user/list?start=0&page_size=1000",
    )
    assert response.status_code == 200
    assert response.json()["total"] == user_number
    db.truncate_table(name="users")
