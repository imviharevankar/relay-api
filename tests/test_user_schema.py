import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_email_and_password():
    user = UserCreate(email="dev@example.com", password="Str0ngPass")
    assert user.email == "dev@example.com"
    assert user.password == "Str0ngPass"
    assert user.full_name is None


def test_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(email="not an email.com", password="Str0ngPass")
    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("email",)


def test_weak_password():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(email="dev@example.com", password="abc")
    assert "too short" in str(exc_info.value)
