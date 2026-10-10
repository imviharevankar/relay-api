import base64
import json
from datetime import timedelta

import pytest

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_correct_password_verifies():
    hashed = hash_password("S3cret-pass")

    assert hashed != "S3cret-pass"
    assert verify_password("S3cret-pass", hashed) is True


def test_wrong_password_does_not_verify():
    hashed = hash_password("S3cret-pass")

    assert verify_password("another-pass", hashed) is False


def test_same_password_gives_different_hashes():
    first = hash_password("S3cret-pass")
    second = hash_password("S3cret-pass")

    assert first != second  # different random salt each time
    assert verify_password("S3cret-pass", first) is True
    assert verify_password("S3cret-pass", second) is True


def test_token_round_trip_returns_the_subject():
    token = create_access_token("42")

    assert decode_access_token(token) == "42"


def test_expired_token_is_rejected():
    token = create_access_token("42", timedelta(seconds=-1))

    assert decode_access_token(token) is None


def test_tampered_payload_is_rejected():
    token = create_access_token("5")
    header, _payload, signature = token.split(".")
    forged = json.dumps({"sub": "1", "exp": 9999999999}).encode()
    forged_payload = base64.urlsafe_b64encode(forged).rstrip(b"=").decode()

    assert decode_access_token(f"{header}.{forged_payload}.{signature}") is None


def test_token_signed_with_another_secret_is_rejected(monkeypatch):
    token = create_access_token("42")
    assert decode_access_token(token) == "42"

    monkeypatch.setenv("SECRET_KEY", "a-completely-different-secret-key-32-bytes")
    get_settings.cache_clear()

    assert decode_access_token(token) is None


@pytest.mark.parametrize("garbage", ["not-a-jwt", "", "a.b.c", "....", " "])
def test_garbage_tokens_return_none(garbage):
    assert decode_access_token(garbage) is None
