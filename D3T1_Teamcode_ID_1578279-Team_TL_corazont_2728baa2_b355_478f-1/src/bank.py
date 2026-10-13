"""Банк вопросов: чтение файла и подсчёты. Выданный файл, менять не нужно.

Это те же функции, что вы писали во втором дне. Модуль ничего не печатает.

load_bank(path)            -> (список вопросов, число пропущенных строк)
find_question(questions, qid) -> вопрос с этим id или None
question_lines(question)   -> строки вопроса для экрана: текст и варианты
count_levels(questions)    -> {уровень: число}
count_topics(questions)    -> {тема: число}
count_matrix(questions)    -> {тема: {уровень: число}}

Каждый вопрос — словарь:
    {"id": 23, "topic": "списки", "level": 2, "type": "короткий",
     "text": "Что напечатает код?\nitems = [3, 1, 2]\nprint(items[0])",
     "options": [], "answer": "3"}
"""

TOPICS = ["строки", "числа", "списки", "ошибки"]


def is_broken(line):
    if line.strip() == "":
        return True
    fields = line.split(";")
    if len(fields) != 7:
        return True
    return fields[2] not in ["1", "2", "3", "4", "5"]


def load_bank(path):
    with open(path, encoding="utf-8") as source:
        lines = source.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    questions = []
    skipped = 0
    for line in lines[1:]:
        if is_broken(line):
            skipped += 1
            continue
        fields = line.split(";")
        options = []
        if fields[5] != "":
            options = fields[5].split("|")
        questions.append({"id": int(fields[0]), "topic": fields[1], "level": int(fields[2]),
                          "type": fields[3], "text": fields[4].replace("\\n", "\n"),
                          "options": options, "answer": fields[6]})
    return questions, skipped


def find_question(questions, qid):
    for question in questions:
        if question["id"] == qid:
            return question
    return None


def question_lines(question):
    lines = question["text"].split("\n")
    number = 1
    for option in question["options"]:
        lines.append(str(number) + ") " + option)
        number += 1
    return lines


def count_levels(questions):
    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for question in questions:
        counts[question["level"]] += 1
    return counts


def count_topics(questions):
    counts = {}
    for topic in TOPICS:
        counts[topic] = 0
    for question in questions:
        counts[question["topic"]] += 1
    return counts


def count_matrix(questions):
    table = {}
    for topic in TOPICS:
        table[topic] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for question in questions:
        table[question["topic"]][question["level"]] += 1
    return table
