"""API Router v1"""
from fastapi import APIRouter
from src.api.v1 import user
from src.api.v1 import health_check


api_router = APIRouter(prefix="/v1")
api_router.include_router(router=health_check.router, prefix="/health")
api_router.include_router(router=user.router, prefix="/user")
