"""Define Authen APIs"""
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.schemas.auth_schema import TokenSchema
from src.services import AuthService


router = APIRouter()


@router.post(path="", response_model=TokenSchema)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()):
    """User login to get access token

    Args:
        user_credentials(OAuth2PasswordRequestForm): form requires username and password
        auth_service(AuthService): authentication service

    Returns TokenSchema including access_token and token_type
    """
    return await auth_service.authenticate(
        username=user_credentials.username,
        password=user_credentials.password,
    )
