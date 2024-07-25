from src.db.models.base_model import BaseModel
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING


class UserModel(BaseModel):
    __tablename__ = "users"

    name: Mapped[str]
