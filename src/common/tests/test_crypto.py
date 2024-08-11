"""Unit tests for cypto module"""
from src.common.crypto import hash_password, verify_password


def test_hash_password():
    """Test hash_passowrd function"""
    assert hash_password(
        plain_password="fake_pass") == "$2b$12$eeeeeeeeeeeeeeeeeeeeeeygkNOsKYGzwqsDTSqjYxnJCrsR/SqRq"
    assert hash_password(
        plain_password="fake_pass", salt="a" * 22) == "$2b$12$aaaaaaaaaaaaaaaaaaaaaOJNsTD5K1HYL0.QShtCdLLvNwdtWDl5O"


def test_verify_password():
    """Test verify_password function"""
    assert verify_password(
        plain_password="fake_pass", hashed_password="$2b$12$eeeeeeeeeeeeeeeeeeeeeeygkNOsKYGzwqsDTSqjYxnJCrsR/SqRq") is True
    assert verify_password(
        plain_password="fake_pass", hashed_password="$2b$12$aaaaaaaaaaaaaaaaaaaaaOJNsTD5K1HYL0.QShtCdLLvNwdtWDl5O") is True
