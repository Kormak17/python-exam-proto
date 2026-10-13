"""Задание 3. Экзамен: разговор с человеком и итог.

Запуск из корня репозитория:  python3 src/exam.py

Функция main в конце файла уже соединяет части экзамена: загружает вопросы,
спрашивает имя, задаёт вопросы по лесенке, подводит итог и записывает результат.
Тела остальных функций этого файла пока простейшие — их пишет тот, кто взял
Задание 3. Как должен выглядеть экран — materials/screen_rus.md.

Этот файл — точка входа: печатает только он.
"""

import sys

import answers
import bank
import ladder

TEAM = "datasets/team.csv"
BANK = "datasets/bank.csv"
RESULTS = "results.csv"
MAX_QUESTIONS = 10


def load_questions():
    """Все вопросы экзамена одним списком: сначала из TEAM, потом из BANK.

    Если файла нет, ошибку FileNotFoundError здесь не перехватывай:
    её перехватывает main.

    Пока тело простейшее: только выданные вопросы.
    """
    a, _ = bank.load_bank(TEAM)
    b, _ = bank.load_bank(BANK)
    questions = a + b
    return questions


def read_line():
    """Прочитать одну строку, которую ввёл человек.

    Возвращает строку без перевода строки в конце. Если ввод закончился
    (Ctrl+D), возвращает None.

    Пока тело простейшее: конец ввода не отличается от пустой строки.
    """
    line = sys.stdin.readline()
    if line == "":
        print("ввод закончился")
        return None
    else:
        line = line.rstrip("\n")
        return line
    # return sys.stdin.readline().rstrip("\n")


def show_question(number, question):
    """Показать вопрос с номером number, как в materials/screen_rus.md.

    Пока тело простейшее: только текст и варианты.
    """
    print(f'Вопрос {number} из 10')
    if question['type'] == 'один':
        for line in bank.question_lines(question):
            print(line)
        print('Введи номер варианта.')
    elif question['type'] == 'несколько':
        for line in bank.question_lines(question):
            print(line)
        print('Введи номера всех верных вариантов через запятую.')
    elif question['type'] == 'короткий':
        for line in bank.question_lines(question):
            print(line)
        print('Напиши ответ.')



def show_result(result):
    """Показать результат ответа: «Верно.», «Неверно.» или «Нет ответа.».

    Пока тело простейшее: результат как есть.
    """
    if result == 'верно':
        print('Верно.')
    if result == 'неверно':
        print('Неверно.')
    if result == 'нет ответа':
        print('Нет ответа.')


def final_level(history):
    """Итоговый уровень по правилу последнего правильного ответа.

    history — список пар (уровень вопроса, результат) в порядке экзамена,
    например [(1, "верно"), (2, "неверно"), (1, "верно")].

    Возвращает уровень последнего вопроса с результатом "верно"
    или None, если верных ответов не было.

    Пока тело простейшее: всегда None.
    """
    # for i in range(-1, -len(history), 1):
    #     if history[i][1] == 'верно':
    #         return history[i][0]
    # return None
    ans = None
    for item in history:
        if item[1] == 'верно':
            ans = item[0]
    return ans



def final_lines(level, history):
    """Строки итога: «Итог: …» и «Почему: …», как в materials/screen_rus.md.

    level — итоговый уровень или None.

    Пока тело простейшее: только первая строка.
    """
    lst = []
    if level is not None:
        lst.append(f'Итог: уровень {level}.')
        lst.append(f'Почему: последний правильный ответ — на уровне {level}.')
        # return [f'Итог: {level}.',f'Почему: последний правильный ответ — на уровне {level}.']
        return lst
    else:
        lst.append("Итог: не определён.")
        lst.append("Почему: ни одного правильного ответа.")
        # return [f'Итог: не определён.',f'Почему: ни одного правильного ответа.']
        return lst

    return ["Итог: не определён."]


def stable_level(history):
    """Задание 6 (дополнительное). Самый высокий уровень, где у человека
    хотя бы два верных ответа, или None.
    """
    ans = None
    slovar = {1: 0,
              2: 0,
              3: 0,
              4: 0,
              5: 0}
    for item in history:
        lvl = item[0]
        status = item[1]
        if status == 'верно':
            slovar[lvl] += 1
    for key in slovar:
        if slovar[key] >= 2:
            ans = key
    return ans


def stable_lines(level, history):
    """Задание 6 (дополнительное). Строки итога для устойчивого правила."""
    lst = []
    slovar = {1: [0, 0],
              2: [0, 0],
              3: [0, 0],
              4: [0, 0],
              5: [0, 0]}
    for item in history:
        lvl = item[0]
        status = item[1]
        if status == 'верно':
            slovar[lvl][0] += 1
            slovar[lvl][1] += 1
        else:
            slovar[lvl][1] += 1
    if level is not None:
        lst.append(f'Итог: уровень {level}.')
        if level < 5:
            lst.append(f'Почему: уровень {level} — самый высокий, где у тебя '
                       f'{slovar[level][0]} верных ответа ({slovar[level][0]}'
                       f' из {slovar[level][1]})'
                       f'.На уровне {min(int(level) + 1, 5)}'
                       f' верных ответов {slovar[min(int(level)+1, 5)][0]}'
                       f' из {slovar[min(int(level)+1, 5)][1]}.')
        elif level == 5:
            lst.append(f'Почему: уровень {level} — самый'
                       f' высокий, где у тебя {slovar[level][0]}'
                       f' верных ответа ({slovar[level][0]} из {slovar[level][1]}).')
    else:
        lst.append("Итог: не определён.")
        lst.append("Почему: недостаточно правильных ответов")
    return lst


def save_result(name, level, asked, correct):
    """Дописать строку «имя;уровень;задано;верно» в конец файла RESULTS.

    level — число или None; при None в поле уровня пишется «не определён».

    Пока тело простейшее: ничего не записывается.
    """
    if name is None:
        name = ('не определён')
    if level is None:
        level = ('не определён')
    if asked is None:
        asked = ('не определён')
    if correct is None:
        correct = ('не определён')
    res = f'{str(name)};{str(level)};{str(asked)};{str(correct)}\n'

    with open(RESULTS, "a", encoding="utf-8") as target:
        target.write(res)


def main():
    try:
        questions = load_questions()
    except FileNotFoundError as error:
        print("Файл не найден: %s" % error.filename)
        return 1

    print("Как тебя зовут?")
    name = read_line()
    if name is None:
        print("Экзамен не начат.")
        return 0
    name = name.replace(";", " ").strip() or "без имени"

    stable = "--stable" in sys.argv
    level = ladder.START_LEVEL
    asked = []
    history = []
    while len(asked) < MAX_QUESTIONS:
        question = ladder.pick_question(questions, level, asked)
        if question is None:
            break
        asked.append(question["id"])
        print()
        show_question(len(asked), question)
        raw = read_line()
        result = answers.check_answer(question, raw if raw is not None else "")
        show_result(result)
        history.append((question["level"], result))
        level = ladder.next_level(question["level"], result)
        if raw is None:
            break

    if stable:
        result_level = stable_level(history)
        lines = stable_lines(result_level, history)
    else:
        result_level = final_level(history)
        lines = final_lines(result_level, history)
    print()
    for line in lines:
        print(line)
    correct = 0
    for _, result in history:
        if result == "верно":
            correct += 1
    save_result(name, result_level, len(asked), correct)
    return 0


if __name__ == "__main__":
    sys.exit(main())
