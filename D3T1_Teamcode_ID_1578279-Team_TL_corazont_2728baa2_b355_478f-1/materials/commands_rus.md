# Команды по этапам работы

Все команды выполняются из корня репозитория.

## Запуск экзамена

| Что | Команда |
| --- | --- |
| Пройти экзамен | `python3 src/exam.py` |
| То же одной командой (после Задания 3) | `bash run_exam.sh` |
| Экзамен с устойчивым итогом (Задание 6) | `python3 src/exam.py --stable` |
| Экзамен со своим правилом (Задание 7) | `python3 src/exam.py --own` |
| Ответы из файла, а не с клавиатуры | `python3 src/exam.py < answers.txt` |
| Закончить ввод с клавиатуры | Ctrl+D в начале пустой строки |

Файл ответов — обычный текстовый файл: в первой строке имя, дальше по одному ответу в строке.

## Проверка

| Что | Команда |
| --- | --- |
| Все тесты | `python3 testing/run_tests.py` |
| Тесты одного задания | `python3 testing/run_tests.py 1` (или `2`, `3`, `4`, `6`) |
| Экзамен целиком | `python3 testing/run_tests.py всё` |
| Линтер | `python3 src/partner/lint.py src` |
| Проверка формата вопросов команды и повторов номеров | `python3 src/partner/check_bank.py datasets/team.csv datasets/bank.csv` |
| Пустые клетки «тема × уровень» | `python3 src/partner/matrix.py datasets/team.csv datasets/bank.csv` |

## Вопросы команды

Дописать в `team.csv` свои вопросы из второго дня — все строки файла, кроме заголовка:

```
tail -n +2 ПУТЬ_К_ПАПКЕ_ВТОРОГО_ДНЯ/datasets/my_questions.csv >> datasets/team.csv
```

`>>` дописывает в конец файла, не стирая того, что там уже есть. Одиночный `>` стёр бы файл целиком — будь внимателен.

Как получить папку второго дня на компьютер — в `git_scenarios_rus.md`, раздел «Файлы из прошлого репозитория».

## Перед обменом и сдачей

```
git pull
python3 testing/run_tests.py
python3 src/partner/lint.py src
python3 src/partner/check_bank.py datasets/team.csv datasets/bank.csv
python3 src/partner/matrix.py datasets/team.csv datasets/bank.csv
bash run_exam.sh
git push
```
