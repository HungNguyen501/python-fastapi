"""Base Respository module"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel as SchemaBaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.base_model import BaseModel

Model = TypeVar("Model", bound=BaseModel)
SchemaModel = TypeVar("SchemaModel", bound=SchemaBaseModel)


class BaseRepository(ABC, Generic[Model, SchemaModel]):
    """Abtract class for data access and persistence into database"""
    db: AsyncSession
    model: Model

    @abstractmethod
    def __init__(self, model: type[Model], db: AsyncSession = Depends()) -> None:
        """Constructor"""
        self.db = db
        self.model = model

    @abstractmethod
    async def get(self, uuid: UUID) -> SchemaModel:
        """Fetch record from DB based on uuid value"""
        raise NotImplementedError()

    @abstractmethod
    async def create(self, data: SchemaBaseModel):
        """Create a record in database"""
        raise NotImplementedError()

    @abstractmethod
    async def update(self, uuid: UUID, data: SchemaBaseModel):
        """Update record in database"""
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, uuid: UUID):
        """Remove record from database"""
        raise NotImplementedError()
