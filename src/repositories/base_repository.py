from uuid import UUID
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from fastapi import Depends
from pydantic import BaseModel as SchemaBaseModel

from src.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.base_model import BaseModel

Model = TypeVar("Model", bound=BaseModel)
SchemaModel = TypeVar("SchemaModel", bound=SchemaBaseModel)


class BaseRepository(ABC, Generic[Model, SchemaModel]):
    db: AsyncSession
    model: Model

    @abstractmethod
    def __init__(self, model: type[Model], db: AsyncSession = Depends()) -> None:
        self.db = db
        self.model = model

    async def get(self, uuid: UUID) -> SchemaModel:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            raise NotFoundException("Item not in repository")
        return result

    @abstractmethod
    async def create(self, data: SchemaBaseModel) -> SchemaModel:
        # noinspection PyCallingNonCallable
        model_instance: Model = self.model(**data.model_dump())
        self.db.add(model_instance)
        await self.db.commit()
        await self.db.refresh(model_instance)

    @abstractmethod
    async def update(self, uuid: UUID, data: SchemaBaseModel) -> SchemaModel:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            raise NotFoundException("Item not in repository")
        for key, value in data.model_dump().items():
            setattr(result, key, value)
        await self.db.commit()
        await self.db.refresh(result)

    async def delete(self, uuid: UUID)  -> SchemaModel:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            raise NotFoundException
        await self.db.delete(result)
        await self.db.commit()
