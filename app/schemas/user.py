from pydantic import BaseModel, EmailStr, field_validator

from app.validators import validate_password


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:
        problems = validate_password(value)

        if problems:
            raise ValueError(",".join(problems))
        return value
