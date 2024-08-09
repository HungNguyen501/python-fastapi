"""User Reponsitory module"""
from uuid import UUID
from typing import List

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError, IntegrityError
from src.repositories.base_repository import BaseRepository
from src.db.models import UserModel
from src.db.database import get_db_session
from src.schemas.user_schema import UserInDB, UserCreate, UserUpdate


class UserRepository(BaseRepository[UserModel, UserInDB]):
    """UserRepository interacts with users table in database"""
    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        """Constructor"""
        super().__init__(UserModel, db)

    async def get(self, uuid: UUID) -> UserModel:
        """Fetch user record from DB based on uuid value

        Args:
            uuid(UUID): value to look up record

        Returns data of record
        """
        result: UserModel | None = await self.db.get(self.model, uuid)
        return result

    async def create(self, data: UserCreate):
        """Create new user in database

        Args:
            data(SchemaBaseModel): data of record would be inserted
        """
        model_instance: UserModel = self.model(**data.model_dump())
        self.db.add(model_instance)
        await self.db.commit()
        await self.db.refresh(model_instance)

    async def update(self, uuid: UUID, data: UserUpdate):
        """Update user in databases

        Args:
            uuid(UUID): value to look up record
            data(SchemaBaseModel): user data would be updated

        Raises:
            IntegrityError: If data of UserUpdate conficts with table schema
        """
        try:
            result: UserModel | None = await self.db.get(self.model, uuid)
            for key, value in data.model_dump().items():
                setattr(result, key, value)
            await self.db.commit()
            await self.db.refresh(result)
        except IntegrityError as exc:
            raise exc.orig.__cause__

    async def delete(self, uuid: UUID):
        """Remove user from database

        Args:
            uuid(UUID): value to look up record

        Raises:
            TypeError: If result is empty
        """
        result: UserModel | None = await self.db.get(self.model, uuid)
        if not result:
            raise TypeError
        await self.db.delete(result)
        await self.db.commit()

    async def list_users(self, start: int, page_size: int) -> List[UserModel]:
        """Retrieve user list from user table

        Args:
            start(int): offset of record for starting
            page_size(int): maximum record number returned

        Returns list of user models

        Raises:
            DBAPIError: If select stament causes error
        """
        try:
            user_list = await self.db.scalars(select(UserModel).limit(page_size).offset(start))
        except DBAPIError as exc:
            raise exc.orig.__cause__
        return user_list

    async def count_user_number(self,) -> int:
        """Returns count number of users"""
        # pylint: disable=not-callable
        user_count = await self.db.scalar(select(func.count(UserModel.uuid)))
        return user_count
