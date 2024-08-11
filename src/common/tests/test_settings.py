""" Unit test for settings module """
from src.common.settings import get_settings


def test_get_settings():
    """Test get_settings functions"""
    assert get_settings().Config.env_file == ".env"
