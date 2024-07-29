"""Unit tests for user_service module"""
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import DBAPIError
from src.services.user_service import UserService
from src.common.exceptions import NotFoundException, InvalidInputException
from src.schemas.user_schema import UserChangeGeneralResonpse


@pytest.mark.asyncio
async def test_get():
    """Test UserService.get function"""
    mock_user_repo = AsyncMock()
    mock_user_repo.get.side_effect = [DBAPIError(statement="select 1", params='', orig=''), None, {"name": "bob"}]
    mock_user_service = UserService(repository=mock_user_repo)
    # Test in case DBAPIError
    with pytest.raises(InvalidInputException) as exc:
        _ = await mock_user_service.get(uuid="-1")
    assert exc.value.detail == 'Invalid UUID'
    # Test in case NotFoundException
    with pytest.raises(NotFoundException) as exc:
        _ = await mock_user_service.get(uuid="-1")
    assert exc.value.detail == 'User not found'
    # Test with having result
    assert await mock_user_service.get(uuid="-1") == {"name": "bob"}


@pytest.mark.asyncio
async def test_create():
    """Test UserService.create function"""
    mock_user_repo = AsyncMock()
    mock_user_repo.create.return_value = 'done'
    mock_user_service = UserService(repository=mock_user_repo)
    assert await mock_user_service.create(data='dummy') == UserChangeGeneralResonpse(message="created")


@pytest.mark.asyncio
async def test_update():
    """Test UserService.update function"""
    mock_user_repo = AsyncMock()
    mock_user_repo.update.side_effect = [AttributeError(), None]
    mock_user_service = UserService(repository=mock_user_repo)
    # Test in case AttributeError, suppress_error should cover this
    assert await mock_user_service.update(uuid="-1", data="none") == UserChangeGeneralResonpse(message='System errors')
    # Test with having result
    assert await mock_user_service.update(uuid="-1", data="none") == UserChangeGeneralResonpse(message="updated")


@pytest.mark.asyncio
async def test_delete():
    """Test UserService.delete function"""
    mock_user_repo = AsyncMock()
    mock_user_repo.delete.side_effect = [TypeError(), None]
    mock_user_service = UserService(repository=mock_user_repo)
    # # Test in case TypeError, suppress_error should cover this
    assert await mock_user_service.delete(uuid="-1") == UserChangeGeneralResonpse(message="System errors")
    # Test with having result
    assert await mock_user_service.delete(uuid="-1") == UserChangeGeneralResonpse(message="deleted")


@pytest.mark.asyncio
async def test_list_users():
    """Test UserService.list_users function"""
    mock_user_repo = AsyncMock()
    mock_user_repo.count_user_number.return_value = -1
    mock_user_repo.list_users.return_value = ['alice', 'bob']
    mock_user_service = UserService(repository=mock_user_repo)
    assert await mock_user_service.list_users(start=1, page_size=0) == (-1, ['alice', 'bob'])
