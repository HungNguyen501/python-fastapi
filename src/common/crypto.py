"""Crypto module"""
from functools import cache

from passlib.context import CryptContext


@cache
def _get_crypt_context() -> CryptContext:
    """Retrieve crypt context"""
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str, salt: str = "e" * 22):
    """Hash password value"""
    return _get_crypt_context().hash(secret=plain_password, salt=salt)


def verify_password(plain_password: str, hashed_password: str):
    """Compare password with hashed_password"""
    return _get_crypt_context().verify(secret=plain_password, hash=hashed_password)
