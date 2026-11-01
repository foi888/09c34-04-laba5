import sys
from report import render_table_header, render_table_row

def load_input_file(input_file: str) -> list[str]:
    """Чтение файла с точной обработкой исключения."""
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден!")
        sys.exit(1)

def save_results(ok_file: str, errors_file: str, accepted: list, rejected: list):
    """Запись результатов в файлы ok.txt и errors.txt."""
    header = render_table_header()
    separator = "-" * len(header)

    with open(ok_file, "w", encoding="utf-8") as f_ok:
        f_ok.write(header + "\n")
        f_ok.write(separator + "\n")
        for idx, item in enumerate(accepted, start=1):
            f_ok.write(render_table_row(idx, item) + "\n")

    with open(errors_file, "w", encoding="utf-8") as f_err:
        for line_num, raw_str, reason in rejected:
            f_err.write(f"Строка {line_num}: {raw_str} | Причина: {reason}\n")

if __name__ == "__main__":
    pass