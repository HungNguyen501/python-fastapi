"""Unit tests for user_repository module"""
from unittest.mock import AsyncMock, MagicMock

import pytest
from src.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create():
    """Test UserRepository.create function"""
    mock_data = MagicMock()
    mock_db = AsyncMock()
    mock_user_repository = UserRepository(db=mock_db)
    await mock_user_repository.create(data=mock_data)
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called


@pytest.mark.asyncio
async def test_update():
    """Test UserRepository.update function"""
    mock_data = MagicMock()
    mock_db = AsyncMock()
    mock_user_repository = UserRepository(db=mock_db)
    await mock_user_repository.update(uuid="-1", data=mock_data)
    assert mock_db.get.called == 1
    assert mock_db.commit.called == 1
    assert mock_db.refresh.called == 1
    assert mock_data.model_dump.return_value.items.return_value.__iter__.called


@pytest.mark.asyncio
async def test_list_users():
    """Test UserRepository.list_users function"""
    mock_db = AsyncMock()
    mock_db.scalars.return_value = [{"name": "alice"}, {"name": "bob"}]
    mock_user_repository = UserRepository(db=mock_db)
    assert await mock_user_repository.list_users(start=-1, page_size=0) == [{'name': 'alice'}, {'name': 'bob'}]


@pytest.mark.asyncio
async def test_count_user_number():
    """Test UserRepository.count_user_number function"""
    mock_db = AsyncMock()
    mock_db.scalar.return_value = -10
    mock_user_repository = UserRepository(db=mock_db)
    assert await mock_user_repository.count_user_number() == -10
