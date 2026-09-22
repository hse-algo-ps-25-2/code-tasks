#!/usr/bin/env bash
set -euo pipefail
# AI Copilot

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}→ Устанавливаю uv (если ещё нет)...${NC}"
if ! command -v uv &> /dev/null; then
    python3.14 -m pip install --user --upgrade uv
    # Добавляем в PATH на всякий случай
    export PATH="$HOME/.local/bin:$PATH"
else
    echo -e "${GREEN}✓ uv уже установлен${NC}"
fi

echo -e "${YELLOW}→ Синхронизирую зависимости проекта...${NC}"
uv sync

echo -e "${YELLOW}→ Активирую виртуальное окружение...${NC}"
if [[ -f ".venv/bin/activate" ]]; then
    echo -e "${GREEN}Окружение готово. Активируй его командой:${NC}"
    echo -e "  ${GREEN}source .venv/bin/activate${NC}"
else
    echo -e "${YELLOW}Виртуальное окружение не найдено (uv создаст его при необходимости)${NC}"
fi

echo "→ Устанавливаю pre-commit хуки..."
uv run pre-commit install

echo -e "\n${GREEN}✓ Готово! Можно начинать разработку.${NC}"
