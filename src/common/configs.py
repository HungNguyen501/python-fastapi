"""Config"""
import os


class OsVariable:  # pylint: disable=too-few-public-methods
    """Os environment variable keys"""
    POSTGRES_HOST = "POSTGRES_HOST"
    POSTGRES_PORT = "POSTGRES_PORT"
    POSTGRES_USER = "POSTGRES_USER"
    POSTGRES_PASSWORD = "POSTGRES_PASSWORD"
    POSTGRES_DB = "POSTGRES_DB"


class Config:  # pylint: disable=too-few-public-methods
    """Config"""
    @staticmethod
    def get(key):
        """Get os' env variable

        Args:
            key(str):

        Returns:
            variable value
        """
        return os.getenv(key)
