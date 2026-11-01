from validators import parse_line
from storage import load_input_file, save_results
from report import print_report

INPUT_FILE = "anketa.txt"
OK_FILE = "ok.txt"
ERRORS_FILE = "errors.txt"

def main():
    # 1. Чтение файла
    lines = load_input_file(INPUT_FILE)
    total_lines = len(lines)

    accepted = []
    rejected = []

    # 2. Обработка данных
    for line_num, raw_line in enumerate(lines, start=1):
        status, result = parse_line(line_num, raw_line)
        if status is None:
            continue
        elif status is True:
            accepted.append(result)
        else:
            rejected.append(result)

    # Сортировка принятых анкет по ФИО
    accepted.sort(key=lambda x: x["fio"])

    # 3. Печать результатов в консоль
    print_report(accepted, rejected, total_lines)

    # 4. Запись в файлы
    save_results(OK_FILE, ERRORS_FILE, accepted, rejected)

if __name__ == "__main__":
    main()