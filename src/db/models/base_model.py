"""Base data model"""
from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Base class for tables"""
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
