"""Health Schema module"""
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health Response"""
    message: str
