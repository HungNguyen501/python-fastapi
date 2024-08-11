"""Unit tests for user model"""
from unittest.mock import AsyncMock, call

import pytest
from src.api.v1.user import (
    get_user,
    create_user,
    update_user,
    delete_user,
    list_users,
)


@pytest.fixture(name="mock_user_service", scope="session")
def gen_mock_user_service():
    """Mock user service instance"""
    mock_us = AsyncMock()
    mock_us.get.return_value = {"uuid": "fool", "name": "alice"}
    mock_us.create.return_value = {"status": "created"}
    mock_us.update.return_value = {"status": "updated"}
    mock_us.delete.return_value = {"status": "deleted"}
    mock_us.list_users.return_value = {"total": 1, "count": 1, "users": [{"name": "bob"}]}
    yield mock_us


@pytest.mark.asyncio
async def test_get_user(mock_user_service, *_):
    """Test get_user function"""
    assert await get_user(uuid="fool", user_service=mock_user_service) == {"uuid": "fool", "name": "alice"}
    assert mock_user_service.get.call_args == call(uuid='fool')


@pytest.mark.asyncio
async def test_create_user(*_):
    """Test get_user function"""
    mock_auth_service = AsyncMock()
    mock_auth_service.create.return_value = {"status": "created"}
    assert await create_user(data={"name": "bob"}, auth_service=mock_auth_service) == {"status": "created"}
    assert mock_auth_service.create.call_args == call(data={'name': 'bob'})


@pytest.mark.asyncio
async def test_update_user(mock_user_service, *_):
    """Test get_user function"""
    assert await update_user(
        uuid="fool",
        data={"name": "bob"},
        user_service=mock_user_service,
    ) == {"status": "updated"}
    assert mock_user_service.update.call_args == call(
        uuid="fool",
        data={"name": "bob"},
    )


@pytest.mark.asyncio
async def test_delete_user(mock_user_service, *_):
    """Test get_user function"""
    assert await delete_user(
        uuid="fool",
        user_service=mock_user_service,
    ) == {"status": "deleted"}
    assert mock_user_service.delete.call_args == call(uuid="fool",)


@pytest.mark.asyncio
async def test_list_user(mock_user_service, *_):
    """Test get_user function"""
    assert await list_users(
        start=-1,
        page_size=-10,
        user_service=mock_user_service,
    ) == {"total": 1, "count": 1, "users": [{"name": "bob"}]}
    assert mock_user_service.list_users.call_args == call(
        start=-1,
        page_size=-10,)
