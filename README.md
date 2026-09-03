# Задания по программированию для курса «Алгоритмы и структуры данных» 💻

Реализация на **Python 3.14**, среда — [Visual Studio Code](https://code.visualstudio.com/).

Инструкции курса (репозиторий [doc](https://github.com/hse-algo-ps-25-2/doc)):

- [Установка необходимого ПО](https://github.com/hse-algo-ps-25-2/doc/blob/main/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B5%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B8%D0%BC%D0%BE%D0%B3%D0%BE%20%D0%9F%D0%9E.md) — GitHub, Git, Python 3.14, VS Code, клонирование, `.venv`
- [Выполнение задания по программированию](https://github.com/hse-algo-ps-25-2/doc/blob/main/%D0%92%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E.md) — ветка, тесты, flake8, pull request
- [Структура ветвления](https://github.com/hse-algo-ps-25-2/doc/blob/main/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D1%8B%20%D0%B2%D0%B5%D1%82%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D1%80%D1%83%D1%87%D0%BD%D1%8B%D1%85%20%D0%B8%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D1%8B%D1%85%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87.md) — чем программные задания отличаются от ручных

## С чего начать

1. Настроить рабочее место по инструкции по установке ПО и **клонировать этот репозиторий** (`code-tasks`).
2. Создать окружение `.venv` на Python 3.14 и выполнить `pip install -r requirements.txt` (только в терминале с префиксом `(.venv)`).
3. Не коммитить решения в `main` и не добавлять `.venv` в репозиторий.

Ручные задания сдаются в отдельном репозитории [manual-tasks](https://github.com/hse-algo-ps-25-2/manual-tasks), окружение Python там не нужно.

## Задания

Условия лежат в ветках с префиксом `main`, например [main-task-0](https://github.com/hse-algo-ps-25-2/code-tasks/tree/main-task-0). Что именно реализовать и какие тесты запускать — в `README.md` **ветки задания**.

Для выполнения создайте свою ветку от ветки задания, подставив название команды вместо префикса `main`, например `first-team-task-0`. На старте курса правки обычно в `main.py`, тесты — в файлах `test_*.py` и в `test_runner.py`.

## Результат выполнения задания: pull request

Подробные шаги и скриншоты — в [инструкции по выполнению](https://github.com/hse-algo-ps-25-2/doc/blob/main/%D0%92%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E.md). Кратко:

- Перед отправкой: все тесты зелёные, локально проходят `isort`, `black` и `flake8` (зелёные Checks на GitHub **не** означают, что оформление принято).
- Pull request: **base** — ветка задания (`main-task-0`), **compare** — ваша ветка (`first-team-task-0`). Не в `main`.
- Ошибки в Checks исправляют новым коммитом в ту же ветку, **новый** pull request создавать не нужно.
- После ревью запрос **закрывают без слияния** с `main-task-`*. Решение остаётся в ветке команды.

