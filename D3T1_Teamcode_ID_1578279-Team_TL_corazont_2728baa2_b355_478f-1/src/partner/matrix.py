"""Матрица «тема × уровень» по одному или нескольким банкам. Выданная программа.

Запуск из корня репозитория:

    python3 src/partner/matrix.py datasets/team.csv datasets/bank.csv

Печатает, сколько вопросов каждой темы на каждом уровне во всех файлах вместе,
и перечисляет пустые клетки. Если пустых клеток нет, завершается с кодом 0,
иначе — с кодом 1. Испорченные строки не считаются: проверь их check_bank.py.
"""

import sys

TOPICS = ["строки", "числа", "списки", "ошибки"]
LEVELS = ["1", "2", "3", "4", "5"]


def count(paths):
    table = {topic: {level: 0 for level in LEVELS} for topic in TOPICS}
    for path in paths:
        with open(path, encoding="utf-8") as source:
            lines = source.read().split("\n")[1:]
        for line in lines:
            fields = line.split(";")
            if len(fields) == 7 and fields[1] in TOPICS and fields[2] in LEVELS:
                table[fields[1]][fields[2]] += 1
    return table


def main():
    paths = sys.argv[1:]
    if not paths:
        print("Запуск: python3 src/partner/matrix.py ФАЙЛ [ФАЙЛ ...]")
        return 1
    try:
        table = count(paths)
    except FileNotFoundError as error:
        print("Файл не найден: %s" % error.filename)
        return 1
    print("\t".join(["тема"] + LEVELS))
    empty = []
    for topic in TOPICS:
        print("\t".join([topic] + [str(table[topic][level]) for level in LEVELS]))
        empty += ["%s × %s" % (topic, level) for level in LEVELS if table[topic][level] == 0]
    print()
    if empty:
        print("Пустые клетки: " + ", ".join(empty))
        return 1
    print("Пустых клеток нет.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
