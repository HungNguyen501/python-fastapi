"""Fake data"""
import jwt
from faker import Faker


_fake = Faker()


class StringFaker:
    """Fake data ultility functions"""

    @staticmethod
    def random_name() -> str:
        """Random name"""
        return _fake.name()

    @staticmethod
    def random_password() -> str:
        """Random password"""
        return _fake.password()

    @staticmethod
    def random_uuid() -> str:
        """Random uuid"""
        return _fake.uuid4()

    @staticmethod
    def random_token() -> str:
        """Random bearer token"""
        return jwt.encode(
            payload={_fake.name(): _fake.password()},
            key=_fake.binary(),
            algorithm="HS256"
        )
