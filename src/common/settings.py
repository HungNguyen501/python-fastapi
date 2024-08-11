"""Config"""
from functools import cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Store configs in .env file"""
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    REDIS_HOST: str
    REDIS_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:  # pylint: disable=too-few-public-methods
        """Define env_file path"""
        env_file = ".env"


@cache
def get_settings():
    """Retrieve settings"""
    return Settings()
