from pathlib import Path


def search_errors_in_log(file_path, search_keyword, report_path):
    """Функция построчно читает файл и ищет заданное ключевое слово."""
    if not file_path.exists():
        print(f"Ошибка: Файл {file_path.name} не найден!")
        return

    error_counter = 0

    try:
        with open(file_path, "r", encoding="utf-8") as file_obj, \
                open(report_path, "w", encoding="utf-8") as report_file:

            report_file.write(
                f"=== ОТЧЕТ СИСТЕМНОГО АНАЛИЗА: {file_path.name} ===\n"
            )
            report_file.write(
                f"Маркер поиска: '{search_keyword}'\n"
            )

            print(f"=== НАЧИНАЕМ АНАЛИЗ ФАЙЛА: {file_path.name} ===\n")
            print(f"Маркер поиска: {search_keyword}\n")

            for line_num, line in enumerate(file_obj, 1):
                if search_keyword.lower() in line.lower():
                    error_counter += 1
                    clean_line = line.strip()

                    print(f"  [Строка {line_num}]: {clean_line}")
                    report_file.write(
                        f"[Строка {line_num}]: {clean_line}\n"
                    )

            # Финальная статистика
            if error_counter > 0:
                summary = f"\nНайдено совпадений: {error_counter}\n"
            else:
                summary = f"\nМаркер '{search_keyword}' не обнаружен.\n"

            print("\n" + "=" * 40)
            print(summary)
            report_file.write(summary)

        print(
            f"Отчет успешно сохранен на сервере: {report_path.name}"
        )

    except PermissionError:
        print(
            f"Критическая ошибка: "
            f"Нет прав на чтение файла {file_path.name}!"
        )
    except UnicodeDecodeError:
        print(
            f"Ошибка кодировки: "
            f"Не удалось прочитать файл в UTF-8. Проверьте формат."
        )


if __name__ == "__main__":
    SCRIPT_DIR = Path(__file__).resolve().parent
    TARGET_LOG = Path("/var/log/syslog")
    REPORT_FILE = SCRIPT_DIR / "analysis_report.txt"

    search_errors_in_log(TARGET_LOG, "CRITICAL", REPORT_FILE)
