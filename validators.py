from collections import Counter

# Ширины колонок для форматирования таблицы
FIO_WIDTH = 28
EMAIL_WIDTH = 24
PHONE_WIDTH = 18
GROUP_WIDTH = 8

def truncate(text: str, max_len: int) -> str:
    """Обрезает строку до max_len символов с многоточием, если она превышает лимит."""
    if len(text) > max_len:
        return text[: max_len - 1] + "…"
    return text

def validate_fio(fio_raw: str) -> tuple[bool, str]:
    """Проверяет и приведёт ФИО к формату 'Иванов Иван Петрович'."""
    words = [w.capitalize() for w in fio_raw.split()]
    if len(words) < 2:
        return False, "слов в ФИО меньше двух"
    return True, " ".join(words)

def validate_email(email_raw: str) -> tuple[bool, str]:
    """Проверяет корректность email-адреса."""
    email = email_raw.strip().lower()
    if email.count("@") != 1:
        return False, "некорректная почта (не ровно одна '@')"

    user, domain = email.split("@")
    if not user or not domain or "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False, "некорректный формат почтового домена"

    return True, email

def validate_phone(phone_raw: str) -> tuple[bool, str]:
    """Проверяет телефон и возвращает его с замаскированной серединой."""
    digits = "".join(c for c in phone_raw if c.isdigit())
    if len(digits) != 11 or digits[0] not in ("7", "8"):
        return False, f"некорректный телефон (цифр: {len(digits)})"

    masked_phone = f"+7 ({digits[1:4]}) ***-**-{digits[9:11]}"
    return True, masked_phone

def validate_group(group_raw: str) -> tuple[bool, str]:
    """Проверяет и очищает название группы."""
    group = group_raw.strip().lower()
    if not group:
        return False, "пустая группа"
    return True, group

def parse_line(line_num: int, raw_line: str):
    """Парсит и валидирует одну строку анкеты."""
    cleaned_line = raw_line.strip()
    if not cleaned_line:
        return None, None

    parts = raw_line.split(";")
    if len(parts) != 4:
        return False, (line_num, cleaned_line, f"не 4 поля (получено {len(parts)})")

    fio_raw, email_raw, phone_raw, group_raw = parts

    # Проверка ФИО
    is_fio_ok, fio_res = validate_fio(fio_raw)
    if not is_fio_ok:
        return False, (line_num, cleaned_line, fio_res)

    # Проверка почты
    is_email_ok, email_res = validate_email(email_raw)
    if not is_email_ok:
        return False, (line_num, cleaned_line, email_res)

    # Проверка телефона
    is_phone_ok, phone_res = validate_phone(phone_raw)
    if not is_phone_ok:
        return False, (line_num, cleaned_line, phone_res)

    # Проверка группы
    is_group_ok, group_res = validate_group(group_raw)
    if not is_group_ok:
        return False, (line_num, cleaned_line, group_res)

    item = {
        "fio": fio_res,
        "email": email_res,
        "phone": phone_res,
        "group": group_res,
    }
    return True, item

if __name__ == "__main__":
    pass