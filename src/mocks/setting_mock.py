"""Mock settings"""
from typing import Any
from unittest.mock import MagicMock


# pylint: disable=invalid-name,too-many-instance-attributes
class SettingsMock(MagicMock):
    """Mock settings objects"""
    def __init__(self, *args: Any, **kw: Any) -> None:
        super().__init__(*args, **kw)
        self.POSTGRES_USER = "jane"
        self.POSTGRES_PASSWORD = "fake_pass"
        self.POSTGRES_HOST = "local"
        self.POSTGRES_PORT = "-1"
        self.POSTGRES_DB = "dum_db"
        self.REDIS_HOST = "redis_local"
        self.REDIS_PORT = 911
        self.SECRET_KEY = "dum_key"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 5
