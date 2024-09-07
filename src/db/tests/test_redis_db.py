"""Unit tests for redis_db module"""
from unittest.mock import call, patch, AsyncMock

import pytest
from src.mocks import RedisMock, SettingsMock
from src.db.redis_db import RedisPool, get_redis_pool


@pytest.mark.asyncio
@patch(target="src.db.redis_db.get_settings", return_value=SettingsMock())
@patch(target="src.db.redis_db.Redis", return_value=RedisMock())
@patch(target="src.db.redis_db.ConnectionPool", side_effect=AsyncMock())
async def test_redis_pool(mock_connection_pool, *_):
    """Test RedisPool class"""
    async with RedisPool() as pool:
        pool._pool = AsyncMock()  # pylint: disable=protected-access
        await pool.set(key="ping", value="pong")
        assert await pool.get(key="ping") == "pong"
    assert mock_connection_pool.call_args == call(host='redis_local', port=911, decode_responses=True, db=0)


@pytest.mark.asyncio
async def test_get_redis_pool():
    """Test get_redis_pool function"""
    assert await get_redis_pool() is not None
