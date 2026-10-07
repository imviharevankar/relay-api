def validate_password(password: str) -> list[str]:
    errors: list[str] = []

    if len(password) < 8:
        errors.append("too short")

    if not any(char.isdigit() for char in password):
        errors.append("needs a digit")

    if not any(char.isupper() for char in password):
        errors.append("needs an uppercase letter")

    if " " in password:
        errors.append("must not contain spaces")

    return errors
