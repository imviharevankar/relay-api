import pytest

from app.validators import validate_password


@pytest.mark.parametrize(
    ("password", "expected_problem"),
    [
        ("Ab1", "too short"),
        ("NoDigitsHere", "needs a digit"),
        ("lowercase123", "needs an uppercase letter"),
        ("Has Space1", "must not contain spaces"),
    ],
)
def test_reports_specific_problem(password, expected_problem):
    assert expected_problem in validate_password(password)


def test_strong_password_has_no_problems():
    assert validate_password("Str0ngPass") == []


def test_reports_all_problems_at_once():
    assert set(validate_password("")) == {
        "too short",
        "needs a digit",
        "needs an uppercase letter",
    }


def test_exactly_eight_characters_is_valid():
    assert validate_password("Abcdef1g") == []
