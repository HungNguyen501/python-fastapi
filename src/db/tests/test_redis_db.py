"""Unit tests for redis_db module"""
from unittest.mock import call, patch, AsyncMock

import pytest
from src.db.redis_db import RedisPool, get_redis_pool


# pylint: disable=C0115,C0116,W0613,W0212,W0106
class RedisMock:
    """Mock Redis class"""
    async def __aenter__(self,):
        return self

    async def __aexit__(self, *_):
        pass

    async def set(self, name, value, *_):
        pass

    async def get(self, name, *_):
        return "pong"


@pytest.mark.asyncio
@patch(target="src.db.database.get_settings")
@patch(target="src.db.redis_db.Redis", return_value=RedisMock())
@patch(target="src.db.redis_db.ConnectionPool", side_effect=AsyncMock())
async def test_redis_pool(mock_connection_pool, mock_redis, mock_settings, *_):
    """Test RedisPool class"""
    mock_settings.return_value.REDIS_HOST.__str__.return_value = "redis_local"
    mock_settings.return_value.REDIS_PORT.__str__.return_value = "911"
    mock_pool = AsyncMock()
    async with RedisPool() as pool:
        pool._pool = mock_pool
        await pool.set(key="ping", value="pong")
        await pool.get(key="ping") == "pong"
    assert mock_connection_pool.call_args == call(host='127.0.0.1', port=6379, decode_responses=True, db=0)
    assert mock_redis.call_args == call(connection_pool=mock_pool)


@pytest.mark.asyncio
async def test_get_redis_pool():
    """Test get_redis_pool function"""
    assert await get_redis_pool() is not None
