"""Unit tests for database module"""
from unittest.mock import patch, call, AsyncMock, MagicMock

import pytest
from src.db.database import DatabaseConnection, DatabaseSessionManager, get_db_session


@patch(target="src.common.configs.OsVariable")
@patch(
    target="src.common.configs.Config.get",
    side_effect=["jane", "fake", "local", "-1", "dum_db"])
@patch(target="src.db.database.BaseModel")
@patch(target="src.db.database.create_engine")
def test_db_connection(mock_create_engine, mock_base_model, *_):
    """Test db connect/ disconnect  function"""
    with DatabaseConnection() as mock_conn:
        assert mock_create_engine.call_args == call(
            url='postgresql+psycopg2://jane:fake@local:-1/dum_db')
        mock_conn.create_tables()
        assert mock_base_model.metadata.create_all.call_args == call(bind=mock_create_engine())
        mock_conn.drop_tables()
        assert mock_base_model.metadata.drop_all.call_args == call(bind=mock_create_engine())
    assert mock_create_engine.return_value.dispose.assert_called


# pylint: disable=protected-access
@pytest.mark.asyncio
@patch(target="src.common.configs.OsVariable")
@patch(
    target="src.common.configs.Config.get",
    side_effect=["jane", "fake", "local", "-1", "dum_db"])
@patch(target="src.db.database.async_sessionmaker", side_effect=AsyncMock())
@patch(target="src.db.database.create_async_engine", side_effect=AsyncMock())
async def test_get_session(mock_create_async_engine, mock_async_sessionmaker, *_):
    """Test get_session function from DatabaseSessionManager"""
    mock_session_manager = DatabaseSessionManager()
    assert mock_create_async_engine.call_args == call(
        url='postgresql+asyncpg://jane:fake@local:-1/dum_db', pool_size=2
    )
    assert mock_async_sessionmaker.call_args == call(
        autocommit=False,
        bind=mock_session_manager._engine
    )
    # Test with TypeError exception when _sessionmaker is None
    mock_session_manager._sessionmaker = None
    with pytest.raises(TypeError) as exc:
        async with mock_session_manager.get_session(): pass  # noqa: E701 # pylint: disable=multiple-statements
    assert str(exc.value) == 'DatabaseSessionManager is not initialized'
    # Test in case _sessionmaker is not None
    mock_session_manager._sessionmaker = MagicMock()
    mock_session_manager._sessionmaker.return_value = AsyncMock()
    with pytest.raises(ValueError) as exc:
        async with mock_session_manager.get_session():
            raise ValueError("Intent to raise exception")
    assert mock_session_manager._sessionmaker.return_value.rollback.called is True
    assert mock_session_manager._sessionmaker.return_value.close.called is True


@pytest.mark.asyncio
@patch(target="src.db.database.async_sessionmaker", side_effect=AsyncMock())
@patch(target="src.db.database.DatabaseSessionManager", return_value=MagicMock())
async def test_get_db_session(*_):
    """Test get_db_session function"""
    assert len([i async for i in get_db_session()]) > 0
