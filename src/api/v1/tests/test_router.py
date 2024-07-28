"""Unit tests for router module"""
from unittest.mock import patch, call

from src.api.v1.router import get_api_router


@patch(target="src.api.v1.router.health_check")
@patch(target="src.api.v1.router.user")
@patch(target="src.api.v1.router.APIRouter")
def test_get_api_router(mock_api_router, mock_user, mock_health_check):
    """Tets get_api_router function"""
    mock_router = get_api_router()
    assert mock_api_router.call_args == call(prefix="/v1")
    # pylint: disable=no-member
    assert mock_router. \
        include_router.mock_calls == [
            call(router=mock_health_check.router, prefix="/health",),
            call(router=mock_user.router, prefix="/user",),
        ]
