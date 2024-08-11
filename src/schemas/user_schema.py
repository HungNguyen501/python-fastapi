"""Request/ response for User APIs"""
from uuid import UUID
from typing import List

from pydantic import BaseModel


class UserUpdate(BaseModel):
    """User update request"""
    password: str


class UserCreate(BaseModel):
    """User create request"""
    name: str
    password: str


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
