"""Define User APIs"""
from uuid import UUID

from fastapi import APIRouter, Depends
from src.services import AuthService, UserService, get_current_user_uuid
from src.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserInDB,
    UserChangeGeneralResonpse,
)


router = APIRouter()


@router.get(path="", response_model=UserInDB)
async def get_user(uuid: UUID = Depends(get_current_user_uuid), user_service: UserService = Depends()):
    """Get user record from database

    Args:
        uuid(str): uuid of user
        user_service(UserService): service to retrive data

    Returns UserInDB to show user info
    """
    return await user_service.get(uuid=uuid)


@router.post(path="", response_model=UserChangeGeneralResonpse)
async def create_user(data: UserCreate, auth_service: AuthService = Depends()):
    """Insert user record into database

    Args:
        data(UserCreate): store user name
        auth_service(AuthService): authentication service

    Returns insertion status
    """
    return await auth_service.create_user(data=data)


@router.put(path="", response_model=UserChangeGeneralResonpse)
async def update_user(data: UserUpdate, uuid: UUID = Depends(get_current_user_uuid), user_service: UserService = Depends()):
    """Update user info into database

    Args:
        uuid(UUID): uuid of user record
        data(UserUpdate): input values for modification
        user_service(UserService): service to retrive data

    Returns status of update
    """
    return await user_service.update(uuid=uuid, data=data)


@router.delete(path="", response_model=UserChangeGeneralResonpse)
async def delete_user(uuid: UUID = Depends(get_current_user_uuid), user_service: UserService = Depends()):
    """Remove user record from database

    Args:
        uuid(UUID): uuid of user record
        user_service(UserService): service to retrive data

    Returns status of deletion
    """
    return await user_service.delete(uuid=uuid)


@router.get(path="/list",)
async def list_users(start: int = 0, page_size: int = 5, user_service: UserService = Depends()):
    """Show info of multiple users from database

    Args:
        start(int): starting index of record for select in database
        page_size(int): limit number of users for each api call
        user_service(UserService): service to retrive data

    Returns list of users in database based on specific conditions
    """
    return await user_service.list_users(start=start, page_size=page_size)
