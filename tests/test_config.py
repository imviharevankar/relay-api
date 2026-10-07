import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_read_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://u:p@h/db")
    monkeypatch.setenv("SECRET_KEY", "abc")
    settings = Settings(_env_file=None)

    assert settings.database_url == "postgresql+asyncpg://u:p@h/db"
    assert settings.secret_key == "abc"


def test_validation_error_from_env(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None)
    assert "secret_key" in str(exc_info.value)
