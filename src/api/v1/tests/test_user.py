"""Unit tests for user model"""
from unittest.mock import AsyncMock, call

import pytest
from src.api.v1.user import (
    # get_user,
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
    mock_us.list_users.return_value = 1, [{"uuid": "-1", "name": "kevin"}]
    yield mock_us


# @pytest.mark.asyncio
# async def test_get_user(mock_user_service, *_):
#     """Test get_user function"""
#     resp = await get_user(uuid="fool", user_service=mock_user_service)
#     assert mock_user_service.get.call_args == call(uuid='fool')
#     assert resp == {"uuid": "fool", "name": "alice"}


@pytest.mark.asyncio
async def test_create_user(mock_user_service, *_):
    """Test get_user function"""
    resp = await create_user(data={"name": "bob"}, user_service=mock_user_service)
    assert mock_user_service.create.call_args == call(data={'name': 'bob'})
    assert resp == {"status": "created"}


@pytest.mark.asyncio
async def test_update_user(mock_user_service, *_):
    """Test get_user function"""
    resp = await update_user(
        uuid="fool",
        data={"name": "bob"},
        user_service=mock_user_service,
    )
    assert mock_user_service.update.call_args == call(
        uuid="fool",
        data={"name": "bob"},
    )
    assert resp == {"status": "updated"}


@pytest.mark.asyncio
async def test_delete_user(mock_user_service, *_):
    """Test get_user function"""
    resp = await delete_user(
        uuid="fool",
        user_service=mock_user_service,
    )
    assert mock_user_service.delete.call_args == call(uuid="fool",)
    assert resp == {"status": "deleted"}


@pytest.mark.asyncio
async def test_list_user(mock_user_service, *_):
    """Test get_user function"""
    resp = await list_users(
        start=-1,
        page_size=-10,
        user_service=mock_user_service,
    )
    assert mock_user_service.delete.call_args == call(uuid="fool",)
    assert resp == {
        "total": 1,
        "count": 1,
        "users": [{"uuid": "-1", "name": "kevin"}],
    }
