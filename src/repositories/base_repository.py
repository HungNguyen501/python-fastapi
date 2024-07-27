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

    async def get(self, uuid: UUID) -> SchemaModel:
        """Fetch record from DB based on uuid value

            Args:
                uuid(UUID): value to look up record

            Returns data of record
        """
        result: Model | None = await self.db.get(self.model, uuid)
        return result

    @abstractmethod
    async def create(self, data: SchemaBaseModel):
        """Create a record in database

        Args:
            data(SchemaBaseModel): data of record would be inserted
        """
        model_instance: Model = self.model(**data.model_dump())
        self.db.add(model_instance)
        await self.db.commit()
        await self.db.refresh(model_instance)

    @abstractmethod
    async def update(self, uuid: UUID, data: SchemaBaseModel):
        """Update record based on its uuid

        Args:
            uuid(UUID): value to look up record
            data(SchemaBaseModel): data would be updated
        """
        result: Model | None = await self.db.get(self.model, uuid)
        for key, value in data.model_dump().items():
            setattr(result, key, value)
        await self.db.commit()
        await self.db.refresh(result)

    async def delete(self, uuid: UUID):
        """Remove record fro database

        Args:
            uuid(UUID): value to look up record
        """
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            raise TypeError
        await self.db.delete(result)
        await self.db.commit()
