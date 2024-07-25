from functools import cache
import contextlib
from typing import AsyncIterator, Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy import create_engine
from src.db.models import BaseModel

    
def create_tables():
    BaseModel.metadata.create_all(create_engine(url=f"postgresql+psycopg2://local:local@localhost:5432/local"))


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine = create_async_engine(url=url, pool_size=2)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@cache
def _get_session_manager():
    return DatabaseSessionManager(url="postgresql+asyncpg://local:local@localhost:5432/local")


async def get_db_session():
    async with _get_session_manager().session() as session:
        yield session

# DbSession = Annotated[AsyncSession, Depends(get_db_session)]
