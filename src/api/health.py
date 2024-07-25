"""Health API"""
from fastapi import APIRouter
from src.schemas.health_schema import HealthResponse


router = APIRouter()

@router.get(path="/")
async def get_health():
    return HealthResponse(message="200 OK")
