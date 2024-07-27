"""Define abstract class for BaseService"""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Generic, TypeVar

from pydantic import BaseModel
from src.repositories.base_repository import BaseRepository

Repository = TypeVar("Repository", bound=BaseRepository)


class BaseService(ABC, Generic[Repository]):
    """Abstract class define business logics"""
    repository: Repository

    @abstractmethod
    def __init__(self, repository: Repository):
        """Constructor"""
        raise NotImplementedError()

    @abstractmethod
    async def get(self, uuid: UUID) -> BaseModel:
        """Retrive data based on UUID value"""
        raise NotImplementedError()

    @abstractmethod
    async def create(self, data: BaseModel) -> BaseModel:
        """Create data entity"""
        raise NotImplementedError()

    @abstractmethod
    async def update(self, uuid: UUID, data: BaseModel) -> BaseModel:
        """Update data entity based on UUID value"""
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, uuid: UUID) -> None:
        """Remove data entity based on UUID value"""
        raise NotImplementedError()
