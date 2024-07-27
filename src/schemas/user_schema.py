"""Request/ response for User APIs"""
from uuid import UUID
from typing import List

from pydantic import BaseModel


class UserUpdate(BaseModel):
    """User update request"""
    name: str | None = None


class UserCreate(UserUpdate):
    """User create request"""
    name: str


class UserInDB(UserCreate):
    """User get response"""
    uuid: UUID


class UserChangeGeneralResonpse(BaseModel):
    """User change (CRUD) general response"""
    message: str


class UserListResponse(BaseModel):
    """User list response"""
    total: int
    count: int
    users: List[UserInDB]
