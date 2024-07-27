"""User Responsitory model"""
from uuid import UUID
from typing import List

from fastapi import Depends

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.db.models.user_model import UserModel
from src.db.database import get_db_session
from src.schemas.user_schema import UserInDB, UserCreate, UserUpdate


class UserRepository(BaseRepository[UserModel, UserInDB]):
    """UserRespository interacts with User table"""
    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        """Constructor"""
        super().__init__(UserModel, db)

    async def create(self, data: UserCreate):
        """Create user"""
        await super().create(data)

    async def update(self, uuid: UUID, data: UserUpdate):
        """Update user"""
        await super().update(uuid, data)

    async def list_users(self, start: int, page_size: int) -> List[UserModel]:
        """Return list of user records"""
        user_list = await self.db.scalars(select(UserModel).limit(page_size).offset(start))
        return list(user_list)

    async def count_user_number(self,) -> int:
        """Return user count"""
        # pylint: disable=not-callable
        user_count = await self.db.scalar(select(func.count(UserModel.uuid)))
        return user_count
