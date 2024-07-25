"""User APIs"""
from uuid import UUID

from fastapi import APIRouter, Depends
from src.schemas.user_schema import UserCreate, UserUpdate, UserInDB, UserChangeGeneralResonpse
from src.services.user_service import UserService


router = APIRouter()

@router.get(path="", response_model=UserInDB)
async def get_user(uuid: str, user_service: UserService = Depends()) -> UserInDB:
    return await user_service.get(uuid=uuid)

@router.post(path="", response_model=UserChangeGeneralResonpse)
async def create_user(data: UserCreate, user_service: UserService = Depends()) -> UserChangeGeneralResonpse:
    return await user_service.create(data=data)

@router.put(path="", response_model=UserChangeGeneralResonpse)
async def update_user(uuid: UUID, data: UserUpdate, user_service: UserService = Depends()) -> UserChangeGeneralResonpse:
    return await user_service.update(uuid=uuid, data=data)

@router.delete(path="", response_model=UserChangeGeneralResonpse)
async def delete_user(uuid: UUID, user_service: UserService = Depends()) -> UserChangeGeneralResonpse:
    return await user_service.delete(uuid=uuid)
