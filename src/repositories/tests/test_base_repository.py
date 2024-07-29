"""Unit tests for base_repository module"""
from unittest.mock import call, MagicMock, AsyncMock

import pytest
from src.repositories.base_repository import BaseRepository


@pytest.fixture(name="mock_base_repo", scope="session")
def gen_mock_base_repo():
    """Create BaseRepository Mock """
    mock_model = MagicMock()
    mock_db = AsyncMock()
    BaseRepository.__abstractmethods__ = frozenset()
    yield BaseRepository(model=mock_model, db=mock_db)  # pylint: disable=abstract-class-instantiated


@pytest.mark.asyncio
async def test_get(mock_base_repo):
    """Test BaseRepository.get function"""
    _ = await mock_base_repo.get(uuid="1")
    assert mock_base_repo.db.get.call_args == call(mock_base_repo.model, '1')


@pytest.mark.asyncio
async def test_delete(mock_base_repo):
    """Test BaseRepository.delete function"""
    mock_base_repo.db.get.return_value.__bool__.return_value = False
    # Test in case result is None
    with pytest.raises(TypeError):
        _ = await mock_base_repo.delete(uuid="1")
    # Test with having result
    mock_base_repo.db.get.return_value.__bool__.return_value = True
    _ = await mock_base_repo.delete(uuid="1")
    assert mock_base_repo.db.delete.called
    assert mock_base_repo.db.commit.called
