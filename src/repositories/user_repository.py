from uuid import UUID

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.db.models import UserModel
from src.db.database import get_db_session
from src.schemas.user_schema import UserInDB, UserCreate, UserUpdate


class UserRepository(BaseRepository[UserModel, UserInDB]):
    def __init__(self, db:AsyncSession = Depends(get_db_session)) -> None:
        super().__init__(UserModel, db)

    async def create(self, data: UserCreate):
        await super().create(data)

    async def update(self, uuid: UUID, data: UserUpdate):
        await super().update(uuid, data)
