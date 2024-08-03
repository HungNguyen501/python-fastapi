"""User Reponsitory module"""
from uuid import UUID
from typing import List

from fastapi import Depends

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from src.repositories.base_repository import BaseRepository
from src.db.models import UserModel
from src.db.database import get_db_session
from src.schemas.user_schema import UserInDB, UserCreate, UserUpdate


class UserRepository(BaseRepository[UserModel, UserInDB]):
    """UserRepository interacts with User table in database"""
    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        """Constructor"""
        super().__init__(UserModel, db)

    async def create(self, data: UserCreate):
        """Create new user"""
        await super().create(data)

    async def update(self, uuid: UUID, data: UserUpdate):
        """Update user"""
        await super().update(uuid, data)

    async def list_users(self, start: int, page_size: int) -> List[UserModel]:
        """Retrieve user list from user table

        Args:
            start(int): offset of record for starting
            page_size(int): maximum record number returned

        Returns list of user models
        """
        try:
            user_list = await self.db.scalars(select(UserModel).limit(page_size).offset(start))
        except DBAPIError as exc:
            raise exc.orig.__cause__
        return list(user_list)

    async def count_user_number(self,) -> int:
        """Returns user count"""
        # pylint: disable=not-callable
        user_count = await self.db.scalar(select(func.count(UserModel.uuid)))
        return user_count
