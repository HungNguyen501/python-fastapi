"""Unit tests for user_service module"""
# pylint: disable=wrong-import-position
from unittest.mock import AsyncMock

import pytest
from asyncpg.exceptions import InvalidRowCountInLimitClauseError, NotNullViolationError, UniqueViolationError
from sqlalchemy.exc import DBAPIError
from src.services.user_service import UserService
from src.common.exceptions import NotFoundException, InvalidInputException
from src.schemas.user_schema import UserInDB, UserCreate, UserUpdate


@pytest.fixture(name="mock_user_repo", scope="session")
def gen_user_repo_mock():
    """Create UserRepository Mock"""
    mock_user_repo = AsyncMock()
    yield mock_user_repo


@pytest.mark.asyncio
async def test_get_user(mock_user_repo):
    """Test UserService.get function"""
    mock_user_repo.get.side_effect = [DBAPIError(statement="select 1 from none", params='', orig=''), None, {"name": "bob"}]
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
async def test_create_user(mock_user_repo):
    """Test UserService.create function"""
    mock_data = UserCreate(name="bob", password="fake_pass")
    mock_user_repo.create.return_value = 'done'
    mock_user_service = UserService(repository=mock_user_repo)
    mock_user_repo.create.side_effect = [True, UniqueViolationError("username is duplicated")]
    assert await mock_user_service.create(data=mock_data) is True
    # Test in case: insert duplicated username
    with pytest.raises(InvalidInputException):
        await mock_user_service.create(data=mock_data)


@pytest.mark.asyncio
async def test_update_user(mock_user_repo):
    """Test UserService.update function"""
    mock_data = UserUpdate(password="fake_pass")
    mock_none_pass_data = UserUpdate(password="")
    mock_user_repo.update.side_effect = [AttributeError(), NotNullViolationError("wrong field name"), None]
    mock_user_service = UserService(repository=mock_user_repo)
    # Test in case AttributeError
    with pytest.raises(NotFoundException):
        await mock_user_service.update(uuid="-1", data=mock_data)
    # Test in case NotNullViolationError
    with pytest.raises(InvalidInputException):
        await mock_user_service.update(uuid="-1", data=mock_none_pass_data)
    # Test with having result
    result = await mock_user_service.update(uuid="-1", data=mock_data)
    assert result.message == "updated"


@pytest.mark.asyncio
async def test_delete_user(mock_user_repo):
    """Test UserService.delete function"""
    mock_user_repo.delete.side_effect = [TypeError(), None]
    mock_user_service = UserService(repository=mock_user_repo)
    # # Test in case TypeError
    with pytest.raises(NotFoundException):
        await mock_user_service.delete(uuid="-1")
    # Test with having result
    result = await mock_user_service.delete(uuid="-1")
    assert result.message == "deleted"


@pytest.mark.asyncio
async def test_list_users(mock_user_repo):
    """Test UserService.list_users function"""
    mock_user_list = [
        UserInDB(uuid="accfd78c-f0dc-4683-90bb-d63de643e850", name="alice", password="123"),
        UserInDB(uuid="accfd78c-f0dc-4683-90bb-d63de643e851", name="bob", password="123")]
    mock_user_repo.count_user_number.return_value = -1
    mock_user_repo.list_users.side_effect = [InvalidRowCountInLimitClauseError("zombie"), mock_user_list]
    mock_user_service = UserService(repository=mock_user_repo)
    with pytest.raises(InvalidInputException):
        await mock_user_service.list_users(start=1, page_size=0)
    result = await mock_user_service.list_users(start=1, page_size=0)
    assert result.total == -1
    assert result.count == 2
    assert result.users == mock_user_list
