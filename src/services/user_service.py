from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from src.services.base_service import BaseService
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreate, UserUpdate, UserInDB, UserChangeGeneralResonpse
from src.exceptions import NotFoundException
from loguru import logger


class UserService(BaseService):
    def __init__(self, repository: UserRepository = Depends()):
        self.repository = repository

    async def get(self, uuid: UUID) -> UserInDB:
        try:
            result = await self.repository.get(uuid)
        except NotFoundException(detail="User not found.") as e:
            logger.error(e)
            return e
        return result

    async def create(self, data: UserCreate) -> UserChangeGeneralResonpse:
        await self.repository.create(data)
        return UserChangeGeneralResonpse(message="created")

    async def update(self, uuid: UUID, data: UserUpdate) -> UserChangeGeneralResonpse:
        try:
            await self.repository.update(uuid, data)
        except NotFoundException(detail="User not found.") as e:
            logger.error(e)
            raise
        return UserChangeGeneralResonpse(message="updated")

    async def delete(self, uuid: UUID) -> UserChangeGeneralResonpse:
        try:
            result = await self.repository.delete(uuid)
        except NotFoundException(detail="User not found.") as e:
            logger.error(e)
            raise
        return UserChangeGeneralResonpse(message="deleted")
