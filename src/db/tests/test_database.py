"""Unit tests for database module"""
from unittest.mock import patch, call, AsyncMock, MagicMock

import pytest
from src.mocks import SettingsMock
from src.db.database import DatabaseConnection, DatabaseSessionManager, get_db_session


@patch(target="src.db.database.get_settings", return_value=SettingsMock())
@patch(target="src.db.database.BaseModel")
@patch(target="src.db.database.create_engine")
def test_db_connection(mock_create_engine, mock_base_model, *_):
    """Test db connect/ disconnect  function"""
    with DatabaseConnection() as mock_conn:
        assert mock_create_engine.call_args == call(
            url='postgresql+psycopg2://jane:fake_pass@local:-1/dum_db')
        mock_conn.create_tables()
        assert mock_base_model.metadata.create_all.call_args == call(bind=mock_create_engine())
        mock_conn.drop_tables()
        assert mock_base_model.metadata.drop_all.call_args == call(bind=mock_create_engine())
    assert mock_create_engine.return_value.dispose.assert_called


# pylint: disable=protected-access
@pytest.mark.asyncio
@patch(target="src.db.database.get_settings", return_value=SettingsMock())
@patch(target="src.db.database.async_sessionmaker", side_effect=AsyncMock())
@patch(target="src.db.database.create_async_engine", side_effect=AsyncMock())
async def test_init_database_sessionmanager(mock_create_async_engine, mock_async_sessionmaker, *_):
    """Test DatabaseSessionManager constructor"""
    mock_session_manager = DatabaseSessionManager()
    assert mock_create_async_engine.call_args == call(
        url='postgresql+asyncpg://jane:fake_pass@local:-1/dum_db', pool_size=2
    )
    assert mock_async_sessionmaker.call_args == call(
        autocommit=False,
        bind=mock_session_manager._engine
    )


@pytest.mark.asyncio
@patch(target="src.db.database.get_settings")
@patch(target="src.db.database.async_sessionmaker", side_effect=AsyncMock())
@patch(target="src.db.database.create_async_engine", side_effect=AsyncMock())
async def test_get_session(*_):
    """Test get_session function in DatabaseSessionManager"""
    mock_session_manager = DatabaseSessionManager()
    # In case: _sessionmaker is None that should raise TypeError exception
    mock_session_manager._sessionmaker = None
    with pytest.raises(TypeError) as exc:
        async with mock_session_manager.get_session(): pass  # noqa: E701 # pylint: disable=multiple-statements
    assert str(exc.value) == 'DatabaseSessionManager is not initialized'
    # In case: _sessionmaker is not None
    mock_session_manager._sessionmaker = MagicMock()
    mock_session_manager._sessionmaker.return_value = AsyncMock()
    with pytest.raises(ValueError) as exc:
        async with mock_session_manager.get_session():
            raise ValueError("Intent to raise exception")
    assert mock_session_manager._sessionmaker.return_value.rollback.called is True
    assert mock_session_manager._sessionmaker.return_value.close.called is True


@pytest.mark.asyncio
@patch(target="src.db.database.get_settings")
@patch(target="src.db.database.async_sessionmaker", side_effect=AsyncMock())
@patch(target="src.db.database.create_async_engine", side_effect=AsyncMock())
async def test_close_db_ss_manager(*_):
    """Test close function in DatabaseSessionManager"""
    # In case: _engine is None along with context manager
    with pytest.raises(TypeError):
        async with DatabaseSessionManager() as mock_session_manager:
            mock_session_manager._engine = None
    # In case: disconnection succeeds
    DatabaseSessionManager.cache_clear()  # pylint: disable=no-member
    mock_session_manager = DatabaseSessionManager()
    mock_session_manager._engine = AsyncMock()
    await mock_session_manager.close()
    assert mock_session_manager._engine is None
    assert mock_session_manager._sessionmaker is None


@pytest.mark.asyncio
@patch(target="src.db.database.async_sessionmaker", side_effect=AsyncMock())
@patch(target="src.db.database.DatabaseSessionManager", return_value=MagicMock())
async def test_get_db_session(*_):
    """Test get_db_session function"""
    assert len([i async for i in get_db_session()]) > 0
