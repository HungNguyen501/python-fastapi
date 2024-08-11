""" Unit test for settings module """
from unittest.mock import patch, call

from src.common.settings import get_settings


@patch(target="src.common.settings.Settings")
def test_get_settings(mock_settings):
    """Test get_settings functions"""
    get_settings()
    assert mock_settings.call_args == call()
