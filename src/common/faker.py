"""Fake data"""
from faker import Faker


fake = Faker()


def random_name() -> str:
    """Random name"""
    return fake.name()


def random_password() -> str:
    """Random password"""
    return fake.password()
