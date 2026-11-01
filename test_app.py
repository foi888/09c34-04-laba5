import pytest
from validators import (
    validate_fio,
    validate_email,
    validate_phone,
    validate_group,
    parse_line,
    truncate
)

# Тестируем обрезку строк (truncate)
def test_truncate():
    assert truncate("Привет", 10) == "Привет"
    assert truncate("ДлиннаяСтрока", 6) == "Длинн…"


# Тестируем проверку ФИО
@pytest.mark.parametrize("raw_fio, expected_ok, expected_res", [
    ("иванов иван петрович", True, "Иванов Иван Петрович"),
    ("петров пётр", True, "Петров Пётр"),
    ("односложное", False, "слов в ФИО меньше двух"),
])
def test_validate_fio(raw_fio, expected_ok, expected_res):
    ok, res = validate_fio(raw_fio)
    assert ok == expected_ok
    assert res == expected_res


# Тестируем проверку Email
@pytest.mark.parametrize("raw_email, expected_ok", [
    ("test@example.com", True),
    ("USER@DOMAIN.RU", True),
    ("bad-email.com", False),
    ("too@@many.com", False),
    ("missingdomain@", False),
])
def test_validate_email(raw_email, expected_ok):
    ok, _ = validate_email(raw_email)
    assert ok == expected_ok


# Тестируем проверку телефона
@pytest.mark.parametrize("raw_phone, expected_ok, expected_res", [
    ("+79991234567", True, "+7 (999) ***-**-67"),
    ("8 (911) 555-44-33", True, "+7 (911) ***-**-33"),
    ("12345", False, "некорректный телефон (цифр: 5)"),
    ("7999123456", False, "некорректный телефон (цифр: 10)"),
])
def test_validate_phone(raw_phone, expected_ok, expected_res):
    ok, res = validate_phone(raw_phone)
    assert ok == expected_ok
    assert res == expected_res


# Тестируем проверку группы
def test_validate_group():
    ok, res = validate_group("  IS-21  ")
    assert ok is True
    assert res == "is-21"

    ok, res = validate_group("   ")
    assert ok is False
    assert res == "пустая группа"


# Тестируем парсинг целой строки
def test_parse_line_valid():
    line = "иванов иван;test@mail.ru;+79991234567;is-21"
    status, result = parse_line(1, line)
    assert status is True
    assert result["fio"] == "Иванов Иван"
    assert result["email"] == "test@mail.ru"
    assert result["group"] == "is-21"


def test_parse_line_invalid_fields_count():
    line = "только;два;поля"
    status, result = parse_line(2, line)
    assert status is False
    assert "не 4 поля" in result[2]