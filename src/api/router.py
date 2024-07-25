"""API Router"""
from fastapi import APIRouter
from src.api import health, user


api_router = APIRouter(prefix="/v1")
api_router.include_router(router=health.router, prefix="/health")
api_router.include_router(router=user.router, prefix="/user")
