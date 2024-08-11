"""Authen Schemas"""
from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Token Response"""
    access_token: str
    token_type: str
