from collections import Counter
from validators import FIO_WIDTH, EMAIL_WIDTH, PHONE_WIDTH, GROUP_WIDTH, truncate

def render_table_header() -> str:
    """Формирует строку заголовков таблицы с постоянными ширинами колонок."""
    return (
        f"{'№':<3} "
        f"{'ФИО':<{FIO_WIDTH}} "
        f"{'Почта':<{EMAIL_WIDTH}} "
        f"{'Телефон':<{PHONE_WIDTH}} "
        f"{'Группа':<{GROUP_WIDTH}}"
    )

def render_table_row(idx: int, item: dict) -> str:
    """Формирует строку таблицы с обрезкой длинных значений."""
    fio = truncate(item["fio"], FIO_WIDTH)
    email = truncate(item["email"], EMAIL_WIDTH)
    phone = truncate(item["phone"], PHONE_WIDTH)
    group = truncate(item["group"], GROUP_WIDTH)

    return f"{idx:<3} {fio:<{FIO_WIDTH}} {email:<{EMAIL_WIDTH}} {phone:<{PHONE_WIDTH}} {group:<{GROUP_WIDTH}}"

def print_report(accepted: list, rejected: list, total_lines: int):
    """Выводит всю статистику и результаты в консоль."""
    header = render_table_header()
    separator = "-" * len(header)

    print("=== ПРИНЯТЫЕ АНКЕТЫ ===")
    print(header)
    print(separator)
    for idx, item in enumerate(accepted, start=1):
        print(render_table_row(idx, item))

    print("\n=== ОТКЛОНЁННЫЕ АНКЕТЫ ===")
    for line_num, raw_str, reason in rejected:
        print(f"Строка {line_num:<2} | '{raw_str}' --> [Причина: {reason}]")

    group_stats = Counter(item["group"] for item in accepted)
    print("\n=== ИТОГИ ===")
    print(f"Всего строк в файле: {total_lines}")
    print(f"Принято:           {len(accepted)}")
    print(f"Отклонено:         {len(rejected)}")
    print("Анкет по группам:")
    for grp, count in group_stats.items():
        print(f"  • {grp}: {count}")

if __name__ == "__main__":
    pass