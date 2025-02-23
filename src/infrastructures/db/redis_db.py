"""Redis Connection module"""
from functools import cache
from typing import Any

from redis.asyncio import ConnectionPool, Redis
from src.common.settings import get_settings


@cache
class RedisPool:
    """Redis Connection Pool"""
    def __init__(self,):
        """Constructor"""
        self._host: str = get_settings().REDIS_HOST
        self._port = get_settings().REDIS_PORT
        self._pool: ConnectionPool = None

    async def connect(self):
        """Connect to connection pool"""
        self._pool = ConnectionPool(host=self._host, port=self._port, decode_responses=True, db=0)

    async def disconnect(self):
        """Disconnect pool"""
        await self._pool.disconnect()

    async def set(self, key: Any, value: Any):
        """Insert key to redis"""
        async with Redis(connection_pool=self._pool) as redis_conn:
            await redis_conn.set(name=key, value=value)

    async def get(self, key):
        """Get value from key in redis"""
        async with Redis(connection_pool=self._pool) as redis_conn:
            return await redis_conn.get(name=key)

    async def __aenter__(self,):
        """Enter context manager"""
        await self.connect()
        return self

    async def __aexit__(self, *_):
        """Exit context manager"""
        await self.disconnect()


async def get_redis_pool():
    """Retrieve Redis Connection Pool"""
    async with RedisPool() as redis_pool:
        return redis_pool
