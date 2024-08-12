"""Authentication Service module"""
from datetime import datetime, timedelta, UTC
import json
from typing import Any

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from src.common.crypto import verify_password
from src.common.exceptions import CredentialsException
from src.common.settings import get_settings
from src.db.redis_db import get_redis_pool, RedisPool
from src.schemas.auth_schema import TokenSchema
from src.schemas.user_schema import UserCreate, UserChangeGeneralResonpse
from src.services.base_service import BaseService
from src.services.user_service import UserService


oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth",)


class AuthService:
    """Authentication service"""
    def __init__(self, base_service: BaseService = Depends(UserService), redis_pool: RedisPool = Depends(get_redis_pool)):
        """Constructor"""
        self.redis_pool: RedisPool = redis_pool
        self.base_service = base_service
        self.TOKEN_TYPE = "bearer"  # pylint: disable=invalid-name

    def _create_access_token(self, data: dict):
        """Generate access token from input data along with expires_at attribute

        Args:
            data(dict): input data

        Returns token that JWT encodes input data and extra field expires_at that indicates that expired time of this token.
        """
        expiration_time = datetime.timestamp(datetime.now(UTC) + timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES))
        playload = data.copy()
        playload.update({"expires_at": expiration_time})
        return jwt.encode(
            payload=playload,
            key=get_settings().SECRET_KEY,
            algorithm=get_settings().ALGORITHM
        )

    async def create_user(self, data: UserCreate,):
        """Insert new user into DB and cache user info (uuid) on Redis"""
        new_user = await self.base_service.create(data=data)
        await self.redis_pool.set(
            key=new_user.name,
            value=json.dumps({"uuid": str(new_user.uuid)})
        )
        return UserChangeGeneralResonpse(message="created")

    async def authenticate(self, username: str, password: str,):
        """Authenticate user by username and password

        Args:
            username(str)
            password(str)

        Returns access token of user for further anthentication

        Raises:
            CredentialsException: If username or password is incorrect
        """
        if user_cache := await self.redis_pool.get(key=username):
            user_cache = json.loads(user_cache)
            user_data = await self.base_service.get(uuid=user_cache["uuid"])
            if verify_password(plain_password=password, hashed_password=user_data.password):
                return TokenSchema(
                    access_token=self._create_access_token(data={"uuid": user_cache["uuid"]}),
                    token_type=self.TOKEN_TYPE,
                )
        raise CredentialsException(detail="Incorrect username or password")


async def get_current_user_uuid(token: Any = Depends(oauth2_schema)):
    """Retrieve user uuid from token of user

    Args:
        token(OAuth2PasswordBearer): from user input

    Returns uuid of user

    Raises:
        CredentialsException: If UUID is null or token expried or credentials are invalid
    """
    try:
        payload = jwt.decode(
            jwt=token,
            key=get_settings().SECRET_KEY,
            algorithms=[get_settings().ALGORITHM]
        )
        if "uuid" not in payload:
            raise CredentialsException(detail="Token does not include UUID")
        if payload["expires_at"] < datetime.now(UTC).timestamp():
            raise CredentialsException(detail="Token expires")
        return payload["uuid"]
    except InvalidTokenError as exc:
        raise CredentialsException(detail="Invalid credentials") from exc
