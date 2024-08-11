"""Unit tests for user_repository module"""
from unittest.mock import call, AsyncMock, MagicMock

import pytest
from asyncpg.exceptions import InvalidRowCountInLimitClauseError, NotNullViolationError, UniqueViolationError
from sqlalchemy.exc import DBAPIError, IntegrityError
from src.repositories.user_repository import UserRepository


@pytest.fixture(name="mock_user_repositoy", scope="session")
def gen_mock_user_repositoy():
    """Create UserRepository Mock"""
    mock_db = AsyncMock()
    yield UserRepository(db=mock_db)


@pytest.mark.asyncio
async def test_get(mock_user_repositoy):
    """Test BaseRepository.get function"""
    _ = await mock_user_repositoy.get(uuid="1")
    assert mock_user_repositoy.db.get.call_args == call(mock_user_repositoy.model, '1')


@pytest.mark.asyncio
async def test_delete(mock_user_repositoy):
    """Test BaseRepository.delete function"""
    mock_user_repositoy.db.get.return_value.__bool__.return_value = False
    # Test in case result is None
    with pytest.raises(TypeError):
        _ = await mock_user_repositoy.delete(uuid="1")
    # Test with having result
    mock_user_repositoy.db.get.return_value.__bool__.return_value = True
    _ = await mock_user_repositoy.delete(uuid="1")
    assert mock_user_repositoy.db.delete.called
    assert mock_user_repositoy.db.commit.called


@pytest.mark.asyncio
async def test_create(mock_user_repositoy):
    """Test UserRepository.create function"""
    # Success case
    mock_data = MagicMock()
    await mock_user_repositoy.create(data=mock_data)
    assert mock_user_repositoy.db.add.called
    assert mock_user_repositoy.db.commit.called
    assert mock_user_repositoy.db.refresh.called
    # IntegrityError due to username duplicated
    mock_exception = MagicMock()
    mock_exception.__cause__ = UniqueViolationError("username is duplicated")
    mock_user_repositoy.db.refresh.side_effect = IntegrityError(statement="", params=None, orig=mock_exception)
    with pytest.raises(UniqueViolationError):
        await mock_user_repositoy.create(data=mock_data)


@pytest.mark.asyncio
async def test_update(mock_user_repositoy):
    """Test UserRepository.update function"""
    mock_data = MagicMock()
    mock_exception = MagicMock()
    mock_exception.__cause__ = NotNullViolationError("column does not exist in table")
    mock_user_repositoy.db.refresh.side_effect = IntegrityError(statement="", params=None, orig=mock_exception)
    mock_data.model_dump.return_value = {"name": "bob"}
    with pytest.raises(NotNullViolationError):
        await mock_user_repositoy.update(uuid="-1", data=mock_data)
    assert mock_user_repositoy.db.get.called == 1
    assert mock_user_repositoy.db.commit.called == 1
    assert mock_user_repositoy.db.refresh.called == 1


@pytest.mark.asyncio
async def test_list_users(mock_user_repositoy):
    """Test UserRepository.list_users function"""
    mock_exception = MagicMock()
    mock_exception.__cause__ = InvalidRowCountInLimitClauseError("Limit offset must not be negative")
    mock_user_repositoy.db.scalars.side_effect = [
        DBAPIError(statement="select 1 from none", params=None, orig=mock_exception),
        [{"name": "alice"}, {"name": "bob"}]
    ]
    # In case: db.scalars throws DBAPIError
    with pytest.raises(InvalidRowCountInLimitClauseError):
        await mock_user_repositoy.list_users(start=-1, page_size=0)
    # In case: db.scalars returns data
    assert await mock_user_repositoy.list_users(start=-1, page_size=0) == [{'name': 'alice'}, {'name': 'bob'}]


@pytest.mark.asyncio
async def test_count_user_number(mock_user_repositoy):
    """Test UserRepository.count_user_number function"""
    mock_user_repositoy.db.scalar.return_value = -10
    assert await mock_user_repositoy.count_user_number() == -10
