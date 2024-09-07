"""Declare mock objects"""
from .connection_mock import DbConnectionMock, RedisMock
from .setting_mock import SettingsMock
from .service_mocks import mock_auth_service, mock_user_service, fake_current_user_uuid, make_test_client

__all__ = [
    "DbConnectionMock",
    "RedisMock",
    "SettingsMock",
    "mock_auth_service",
    "mock_user_service",
    "fake_current_user_uuid",
    "make_test_client",
]
