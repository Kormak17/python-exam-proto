"""Тесты экзамена. Выданная программа: читать можно, менять нельзя.

Запуск из корня репозитория:

    python3 testing/run_tests.py        все задания
    python3 testing/run_tests.py 2      только Задание 2

Для каждой части печатается одна строка: «пройдено», «не пройдено» с первой
найденной причиной или «не начато». Строка «Экзамен целиком» запускает
src/exam.py как настоящий экзамен на выданном банке.
"""

import io
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, "src")

ONE = {"id": 1, "topic": "числа", "level": 1, "type": "один",
       "text": "?", "options": ["23", "5", "2 + 3", "ошибка"], "answer": "2"}
MANY = {"id": 2, "topic": "строки", "level": 2, "type": "несколько",
        "text": "?", "options": ["print", "cd", "input", "ls"], "answer": "1,3"}
SHORT = {"id": 3, "topic": "строки", "level": 1, "type": "короткий",
         "text": "?", "options": [], "answer": "strip|strip()"}


class NotStarted(Exception):
    pass


class Failed(Exception):
    pass


def expect(condition, message):
    if not condition:
        raise Failed(message)


def q(qid, level):
    return {"id": qid, "topic": "числа", "level": level, "type": "короткий",
            "text": "?", "options": [], "answer": "1"}


# ------------------------------------------------------------- Задание 1

def task_1():
    import answers
    check = answers.check_answer
    if check(ONE, "2") == "нет ответа" and check(SHORT, "strip") == "нет ответа":
        raise NotStarted()
    cases = [
        (ONE, "2", "верно"), (ONE, "  2 ", "верно"), (ONE, "4", "неверно"),
        (ONE, "5", "неверно"), (ONE, "два", "неверно"), (ONE, "02", "неверно"),
        (ONE, "", "нет ответа"),
        (ONE, "   ", "нет ответа"),
        (MANY, "1,3", "верно"), (MANY, "3, 1", "верно"), (MANY, " 1 , 3 ", "верно"),
        (MANY, "1", "неверно"), (MANY, "1,3,4", "неверно"), (MANY, "1,1,3", "неверно"),
        (MANY, "1,,3", "неверно"), (MANY, "1,03", "неверно"),
        (MANY, "", "нет ответа"),
        (SHORT, "strip", "верно"), (SHORT, "  Strip() ", "верно"), (SHORT, "STRIP", "верно"),
        (SHORT, "split", "неверно"), (SHORT, "st rip", "неверно"), (SHORT, "", "нет ответа"),
    ]
    for question, raw, want in cases:
        got = check(question, raw)
        expect(got == want, "тип «%s», ответ %r: ожидалось «%s», получено «%s»"
               % (question["type"], raw, want, got))


# ------------------------------------------------------------- Задание 2

def task_2():
    import ladder
    if ladder.next_level(1, "верно") == 1 and ladder.next_level(3, "неверно") == 3:
        raise NotStarted()
    expect(ladder.START_LEVEL == 1, "START_LEVEL должен быть 1")
    for level, result, want in [(1, "верно", 2), (4, "верно", 5), (5, "верно", 5),
                                (3, "неверно", 2), (1, "неверно", 1),
                                (3, "нет ответа", 3)]:
        got = ladder.next_level(level, result)
        expect(got == want, "next_level(%d, %r) должна вернуть %d, а вернула %s"
               % (level, result, want, got))
    questions = [q(101, 2), q(1, 1), q(5, 2), q(12, 4), q(13, 4)]

    def pick(level, asked):
        found = ladder.pick_question(questions, level, asked)
        return None if found is None else found["id"]

    expect(pick(2, []) == 101, "на уровне 2 первым должен быть первый по порядку вопрос "
           "этого уровня — вопрос команды 101")
    expect(pick(2, [101]) == 5, "вопрос 101 уже задан — следующий на уровне 2 это 5")
    expect(pick(1, [1]) == 101, "на уровне 1 вопросов нет — ближайший уровень 2, вопрос 101")
    expect(pick(3, [101, 5]) == 12, "уровни 2 и 4 одинаково близки к 3, но на уровне 2 "
           "вопросов не осталось, а уровень 4 ближе уровня 1 — вопрос 12")
    both = [q(21, 2), q(22, 4)]
    found = ladder.pick_question(both, 3, [])
    expect(found is not None and found["id"] == 21,
           "уровни 2 и 4 одинаково близки к 3 — берётся тот, что ниже: вопрос 21")
    expect(ladder.pick_question(questions, 2, [101, 1, 5, 12, 13]) is None,
           "все вопросы заданы — pick_question должна вернуть None")


# ------------------------------------------------------------- Задание 3

def capture(function, *args):
    saved = sys.stdout
    sys.stdout = io.StringIO()
    try:
        function(*args)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = saved


def with_stdin(text, function):
    saved = sys.stdin
    sys.stdin = io.StringIO(text)
    try:
        return function()
    finally:
        sys.stdin = saved


def task_3():
    import exam
    if exam.final_level([(1, "верно")]) is None and \
            exam.final_lines(3, []) == ["Итог: не определён."]:
        raise NotStarted()
    for history, want in [([(1, "верно"), (2, "неверно")], 1),
                          ([(1, "верно"), (2, "верно"), (3, "неверно"), (2, "верно")], 2),
                          ([(1, "верно"), (2, "верно"), (3, "неверно"), (2, "нет ответа")], 2),
                          ([(1, "неверно"), (1, "нет ответа")], None), ([], None)]:
        got = exam.final_level(history)
        expect(got == want, "final_level(%s) должна вернуть %s, а вернула %s"
               % (history, want, got))
    expect(exam.final_lines(3, []) == ["Итог: уровень 3.",
                                       "Почему: последний правильный ответ — на уровне 3."],
           "final_lines(3, …): две строки, как в materials/screen_rus.md")
    expect(exam.final_lines(None, []) == ["Итог: не определён.",
                                          "Почему: ни одного правильного ответа."],
           "final_lines(None, …): две строки, как в materials/screen_rus.md")
    expect(with_stdin("Аня\n", exam.read_line) == "Аня", "read_line должна вернуть строку "
           "без перевода строки")
    expect(with_stdin("\n", exam.read_line) == "", "на пустой строке read_line возвращает \"\"")
    expect(with_stdin("", exam.read_line) is None, "в конце ввода read_line возвращает None")
    shown = capture(exam.show_question, 1, ONE).split("\n")
    expect(shown[:6] == ["Вопрос 1 из 10", "?", "1) 23", "2) 5", "3) 2 + 3", "4) ошибка"]
           and shown[6] == "Введи номер варианта.",
           "show_question: заголовок, текст, варианты и подсказка, как в materials/screen_rus.md")
    expect(capture(exam.show_question, 2, MANY).split("\n")[6] ==
           "Введи номера всех верных вариантов через запятую.",
           "show_question: подсказка для типа «несколько»")
    expect(capture(exam.show_question, 3, SHORT).split("\n")[2] == "Напиши ответ.",
           "show_question: подсказка для типа «короткий»")
    expect(capture(exam.show_result, "нет ответа") == "Нет ответа.\n",
           "show_result: «Нет ответа.» с точкой")
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    # os.remove(path)
    saved = exam.RESULTS
    exam.RESULTS = path
    try:
        exam.save_result("Аня", 3, 10, 6)
        exam.save_result("Боря", None, 2, 0)
        with open(path, encoding="utf-8") as source:
            lines = source.read().split("\n")
    finally:
        exam.RESULTS = saved
        if os.path.exists(path):
            os.remove(path)
    expect(lines[:2] == ["Аня;3;10;6", "Боря;не определён;2;0"],
           "save_result дописывает строки «имя;уровень;задано;верно»; при None — «не определён»")


# ------------------------------------------------------------- Задание 4

TOPICS = ["строки", "числа", "списки", "ошибки"]


def read_rows(path):
    with open(path, encoding="utf-8") as source:
        lines = source.read().split("\n")[1:]
    return [line.split(";") for line in lines if line.strip() != ""]


def task_4():
    team = read_rows(os.path.join("datasets", "team.csv"))
    if not team:
        raise NotStarted()
    expect(all(len(row) == 7 for row in team),
           "в team.csv есть строки не из семи полей — проверь src/partner/check_bank.py")
    expect(10 <= len(team) <= 20, "в team.csv вопросов: %d, а нужно от 10 до 20" % len(team))
    kinds = set(row[3] for row in team)
    for kind in ["один", "несколько", "короткий"]:
        expect(kind in kinds, "в team.csv нет вопросов типа «%s»" % kind)
    cells = set((row[1], row[2]) for row in team + read_rows(os.path.join("datasets", "bank.csv")))
    empty = ["%s × %s" % (topic, level) for topic in TOPICS for level in "12345"
             if (topic, level) not in cells]
    expect(not empty, "пустые клетки «тема × уровень»: " + ", ".join(empty))


# ------------------------------------------------------------- Задание 6

def task_6():
    import exam
    if exam.stable_level([(1, "верно"), (1, "верно")]) is None:
        raise NotStarted()
    for history, want in [([(1, "верно"), (1, "верно")], 1),
                          ([(1, "верно"), (2, "верно"), (3, "верно"), (2, "верно")], 2),
                          ([(1, "верно"), (2, "неверно"), (1, "верно"), (2, "верно")], 1),
                          ([(3, "верно")], None)]:
        got = exam.stable_level(history)
        expect(got == want, "stable_level(%s) должна вернуть %s, а вернула %s"
               % (history, want, got))
    lines = exam.stable_lines(2, [(1, "верно"), (2, "верно"), (2, "верно")])
    expect(len(lines) == 2 and lines[0] == "Итог: уровень 2." and lines[1].startswith("Почему:"),
           "stable_lines(2, …): «Итог: уровень 2.» и строка «Почему: …»")
    lines = exam.stable_lines(None, [(1, "верно")])
    expect(len(lines) == 2 and lines[0] == "Итог: не определён." and
           lines[1].startswith("Почему:"),
           "stable_lines(None, …): «Итог: не определён.» и строка «Почему: …»")


# ------------------------------------------------------------- экзамен целиком

def run_exam(folder, text, extra=(), script=False):
    command = ["bash", "run_exam.sh"] if script else [sys.executable, "src/exam.py"]
    done = subprocess.run(command + list(extra), cwd=folder, input=text,
                          capture_output=True, text=True, timeout=20)
    return done.returncode, done.stdout, done.stderr


def make_copy():
    """Временная копия: src/, run_exam.sh, выданный банк и маленький team.csv."""
    folder = tempfile.mkdtemp()
    shutil.copytree("src", os.path.join(folder, "src"))
    if os.path.isfile("run_exam.sh"):
        shutil.copy("run_exam.sh", folder)
    os.makedirs(os.path.join(folder, "datasets"))
    shutil.copy(os.path.join("datasets", "bank.csv"), os.path.join(folder, "datasets"))
    with open(os.path.join(folder, "datasets", "team.csv"), "w", encoding="utf-8") as team:
        team.write("id;тема;уровень;тип;вопрос;варианты;ответ\n"
                   "101;строки;2;короткий;Командный вопрос?;;да\n")
    return folder


def whole():
    expect(os.path.isfile("run_exam.sh"), "в корне репозитория нет run_exam.sh")
    folder = make_copy()
    try:
        code, out, err = run_exam(folder, "Аня\n2\nда\n", script=True)
        expect(out.startswith("Как тебя зовут?"),
               "bash run_exam.sh должен запускать экзамен: " + (err.strip() or out.strip())[-80:])
        expect("Traceback" not in err, "экзамен упал: " + (err.strip().split("\n") or [""])[-1])
        expect(code == 0, "экзамен завершился с кодом %s" % code)
        expect("Вопрос 2 из 10\nКомандный вопрос?" in out,
               "после верного ответа на уровне 1 второй вопрос — уровня 2, "
               "и первым на уровне идёт вопрос команды")
        code, out, err = run_exam(folder, "Боря\nx\n")
        expect("Вопрос 2 из 10\nКакой метод строки убирает пробелы" in out,
               "после неверного ответа на уровне 1 второй вопрос — снова уровня 1")
        expect(out.rstrip("\n").endswith("Итог: не определён.\nПочему: ни одного правильного "
                                         "ответа."), "итог без верных ответов — «не определён»")
        results = os.path.join(folder, "results.csv")
        expect(os.path.exists(results), "после экзамена в results.csv должна появиться строка")
        with open(results, encoding="utf-8") as source:
            rows = source.read().split("\n")
        expect(rows[:2] == ["Аня;2;3;2", "Боря;не определён;2;0"],
               "строки results.csv: ожидалось «Аня;2;3;2» и «Боря;не определён;2;0», "
               "получено %s" % rows[:2])
        os.remove(results)
        code, out, err = run_exam(folder, "")
        expect(code == 0 and out.strip().endswith("Экзамен не начат.") and
               not os.path.exists(results),
               "Ctrl+D на имени: «Экзамен не начат.», код 0, без записи в results.csv")
        code, out, err = run_exam(folder, "Вера\n" + "2\n" * 30)
        expect(out.count("Вопрос ") == 10, "вопросов должно быть не больше 10")
        import exam
        if exam.stable_level([(1, "верно"), (1, "верно")]) is not None:
            code, out, err = run_exam(folder, "Аня\n2\nx\nstrip\nx\n", ["--stable"], script=True)
            expect(code == 0 and "Итог: уровень 1." in out,
                   "с --stable после двух верных ответов на уровне 1 итог — «Итог: уровень 1.»")
        os.remove(os.path.join(folder, "datasets", "bank.csv"))
        code, out, err = run_exam(folder, "Аня\n")
        expect(code == 1 and "Файл не найден" in out and "Traceback" not in err,
               "без банка — «Файл не найден» и код 1")
    finally:
        shutil.rmtree(folder, ignore_errors=True)


PARTS = [("1", "Задание 1 (answers.py)", task_1), ("2", "Задание 2 (ladder.py)", task_2),
         ("3", "Задание 3 (exam.py)", task_3), ("4", "Задание 4 (team.csv)", task_4),
         ("6", "Задание 6 (дополнительное)", task_6),
         ("всё", "Экзамен целиком", whole)]


def main():
    if not os.path.isdir("src") or not os.path.isfile(os.path.join("src", "exam.py")):
        print("Нет папки src с exam.py. Запускай тесты из корня репозитория.")
        return 1
    only = sys.argv[1] if len(sys.argv) > 1 else None
    chosen = [part for part in PARTS if only is None or part[0] == only]
    if not chosen:
        print("Тесты есть для заданий 1, 2, 3, 4 и 6.")
        return 1
    failed, passed, broken = [], [], False
    for key, name, test in chosen:
        if key == "всё" and only is None and not {"1", "2", "3"} <= set(passed):
            waiting = [number for number in ["1", "2", "3"] if number not in passed]
            print("%s: ждёт заданий %s" % (name, ", ".join(waiting)))
            failed.append(key)
            continue
        try:
            test()
            passed.append(key)
            print("%s: пройдено" % name)
        except NotStarted:
            print("%s: не начато" % name)
            if key != "6":
                failed.append(key)
        except Failed as problem:
            failed.append(key)
            broken = True
            print("%s: не пройдено — %s" % (name, problem))
        except Exception as error:
            failed.append(key)
            broken = True
            print("%s: не пройдено — упало: %s: %s" % (name, type(error).__name__, error))
    if broken:
        print("…помехи… что-то не сходится. Смотри, что возвращает функция. — Э.")
    if failed:
        return 1
    if only is None:
        print("Экзамен собран. Осталось пройти чужой — и пятница уже не страшна. — Э.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
