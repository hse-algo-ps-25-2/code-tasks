.PHONY: help install test lint format format-check check
.DEFAULT_GOAL := help

help:
		@echo "Доступные команды: help"
		@echo "install: Установить зависимости, окружение и pre-commit хуки"
		@echo "test: Запустить модульные тесты"
		@echo "lint: Проверить код линтером Ruff"
		@echo "format: Автоматически отформатировать код через Ruff"
		@echo "format-check: Проверить корректность форматирования"
		@echo "check: Прогнать все проверки перед PR (линтер + форматирование + тесты)"
		@echo "Удалить кэши, артефакты и виртуальное окружение"

install:
		@echo "Установка окружения..."
		./install-dev.sh

test:
		@echo "Запуск тестов..."
		uv run python -m unittest discover -s . -p "test*.py" -v

lint:
		@echo "Проверка кода_Ruff..."
		uv run ruff check .

format:
		@echo "Форматирование кода..."
		uv run ruff format .

format-check:
		@echo "Проверка форматирования"
		uv run ruff format --check .

check: lint format-check test
		@echo "Все проверки успешно пройдены"
