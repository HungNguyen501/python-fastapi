""" Unit test for configs module """
from unittest.mock import patch

from src.common.configs import Config


@patch("os.getenv", return_value='dummy')
def test_os_get(_):
    """ test Config's os_get function """
    assert Config.get("foo") == 'dummy'
