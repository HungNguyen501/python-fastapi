"""Unit tests for hehealh_check module"""
from unittest.mock import patch

import pytest
from src.api.v1.health_check import get_health_check


@pytest.mark.asyncio
@patch(target="src.api.v1.health_check.APIRouter")
async def test_get_health_check(*_):
    """Test get_health_check function"""
    resp = await get_health_check()
    assert resp.message == "200 OK"
