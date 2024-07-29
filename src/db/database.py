"""Database Connection and Session Manager modules"""
from functools import cache
from typing import AsyncIterator
import contextlib

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy import create_engine
from src.common.configs import Config, OsVariable
from src.db.models import BaseModel


class DatabaseConnection:
    """Provide database connection along with Context Manager"""
    def __init__(self,):
        """Constructor"""
        self._url = f"postgresql+psycopg2://" \
                    f"{Config.get(OsVariable.POSTGRES_USER)}:{Config.get(OsVariable.POSTGRES_PASSWORD)}" \
                    f"@{Config.get(OsVariable.POSTGRES_HOST)}:{Config.get(OsVariable.POSTGRES_PORT)}" \
                    f"/{Config.get(OsVariable.POSTGRES_DB)}"
        self._conn = None

    def connect(self,):
        """Connect to DB"""
        self._conn = create_engine(url=self._url)

    def disconnect(self,):
        """Disconnect from DB"""
        self._conn.dispose()

    def create_tables(self,):
        """Create all tables in metadata"""
        BaseModel.metadata.create_all(bind=self._conn)

    def drop_tables(self,):
        """Drop all tables in metadata"""
        BaseModel.metadata.drop_all(bind=self._conn)

    def __enter__(self,):
        """Enter context"""
        self.connect()
        return self

    def __exit__(self, *_):
        """Exit context"""
        self.disconnect()


@cache
class DatabaseSessionManager:  # pylint: disable=too-few-public-methods
    """Session Manager controls database session connections"""
    def __init__(self,):
        """Contructor"""
        self._url = f"postgresql+asyncpg://" \
                    f"{Config.get(OsVariable.POSTGRES_USER)}:{Config.get(OsVariable.POSTGRES_PASSWORD)}" \
                    f"@{Config.get(OsVariable.POSTGRES_HOST)}:{Config.get(OsVariable.POSTGRES_PORT)}" \
                    f"/{Config.get(OsVariable.POSTGRES_DB)}"
        self._engine = create_async_engine(url=self._url, pool_size=2)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """Provision session from session maker"""
        if self._sessionmaker is None:
            raise TypeError("DatabaseSessionManager is not initialized")
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session():
    """Retrive database session from DatabaseSessionManager"""
    session_manager = DatabaseSessionManager()
    async with session_manager.get_session() as session:
        yield session
