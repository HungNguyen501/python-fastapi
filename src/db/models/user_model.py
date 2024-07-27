"""Model for table user"""
from sqlalchemy.orm import Mapped
from src.db.models.base_model import BaseModel


class UserModel(BaseModel):  # pylint: disable=too-few-public-methods
    """Define attributes for User model"""
    __tablename__ = "users"

    name: Mapped[str]
