"""Service module for User entity"""
from typing import Tuple, List
from uuid import UUID

from asyncpg.exceptions import (
    InvalidRowCountInLimitClauseError,
    InvalidRowCountInResultOffsetClauseError,
    NotNullViolationError,
    UniqueViolationError,
)
from fastapi import Depends
from sqlalchemy.exc import DBAPIError
from src.common.crypto import hash_password
from src.exceptions.exception_handler import pegasus
from src.exceptions.exceptions import NotFoundException, InvalidInputException
from src.repositories import UserRepository
from src.services.business.base_service import BaseService
from src.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserInDB,
    UserChangeGeneralResonpse,
    UserListResponse,
)


class UserService(BaseService):
    """Class defines business logics for User entity"""
    def __init__(self, repository: UserRepository = Depends()):
        """Constructor"""
        self.repository = repository

    async def get(self, uuid: UUID) -> UserInDB:
        """Retrive user record by UUID

        Args:
            uuid(UUID): value to look up in DB

        Returns:
            user data as UserInDB

        Raises:
            DBAPIError: If uuid is wrong format
            NotFoundException: If result is empty
        """
        try:
            result = await self.repository.get(uuid)
        except DBAPIError as exc:
            raise InvalidInputException(detail="Invalid UUID") from exc
        if not result:
            raise NotFoundException(detail="User not found")
        return result

    @pegasus(target="create user api", allow_errors=(InvalidInputException,))
    async def create(self, data: UserCreate) -> UserInDB:
        """Create user

        Args:
            data(UserCreate): data would be inserted

        Returns:
            status of insertion

        Raises:
            UniqueViolationError If username is duplicated
        """
        try:
            data.password = hash_password(data.password)
            new_user = await self.repository.create(data)
            return new_user
        except UniqueViolationError as exc:
            raise InvalidInputException(detail=exc.args[0]) from exc

    @pegasus(target="update user api", allow_errors=(NotFoundException, InvalidInputException,))
    async def update(self, uuid: UUID, data: UserUpdate) -> UserChangeGeneralResonpse:
        """Update user data based its UUID

        Args:
            uuid(UUID): value to look up
            data(UserUpdate): data woulbe updated

        Raises:
            AttributeError: If update operation does not find any records
            NotNullViolationError: If data of UserUpdate is invalid
        """
        try:
            if data.password:
                data.password = hash_password(data.password)
            await self.repository.update(uuid, data)
            return UserChangeGeneralResonpse(message="updated")
        except AttributeError as exc:
            raise NotFoundException("User not found") from exc
        except NotNullViolationError as exc:
            raise InvalidInputException(detail=exc.args[0]) from exc

    @pegasus(target="delete user api", allow_errors=NotFoundException,)
    async def delete(self, uuid: UUID) -> UserChangeGeneralResonpse:
        """Remove user data based its UUID

        Args:
            uuid(UUID): value to look up

        Raises:
            TypeError: If delete operation does not find any records
        """
        try:
            await self.repository.delete(uuid)
        except TypeError as exc:
            raise NotFoundException("User not found") from exc
        return UserChangeGeneralResonpse(message="deleted")

    @pegasus(target="list user api", allow_errors=InvalidInputException,)
    async def list_users(self, start: int, page_size: int) -> Tuple[int, List[UserInDB]]:
        """List users in User table

        Args:
            start(int): starting offset for retrieving
            page_size(int): size of pagination

        Returns:
            number of records
            array of user records

        Raises:
            InvalidRowCountInLimitClauseError: If limit value is not valid
            InvalidRowCountInResultOffsetClauseError: If offset value is not valid
        """
        try:
            user_count = await self.repository.count_user_number()
            user_list = [UserInDB(**user.__dict__)
                         for user in await self.repository.list_users(start=start, page_size=page_size)]
        except (InvalidRowCountInLimitClauseError, InvalidRowCountInResultOffsetClauseError) as exc:
            raise InvalidInputException(detail=str(exc)) from exc
        return UserListResponse(
            total=user_count,
            count=len(user_list),
            users=user_list,
        )
