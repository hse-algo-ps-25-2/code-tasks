import random
from enum import StrEnum


class ErrorMessages(StrEnum):
    "Перечисление сообщений об ошибках"

    NOT_LIST_ERROR_MESSAGE = "Набор не является списком"
    LIST_CONTAINS_NOT_COMPARABLE_ITEMS =\
        "Список содержит не сравнимые оператором < элементы"


def __check_constrains(items: list):
    "Проверка условий"

    if not isinstance(items, list):
        raise TypeError(ErrorMessages.NOT_LIST_ERROR_MESSAGE)


def recursive_quicksort(items: list) -> list:
    """Возвращает новый список, упорядоченный по неубыванию.
    Алгоритм — Быстрая сортировка (QuickSort).

    :param items: список сравнимых элементов.\
        Элементы должны быть попарно сравнимы операцией <.
    :raise TypeError: если items не список либо элементы несравнимы
    :return: новый отсортированный список
    """
    __check_constrains(items)
    try:
        return __recursive_quicksort(items, 0, len(items) - 1)
    except TypeError as exception:
        raise TypeError(ErrorMessages.LIST_CONTAINS_NOT_COMPARABLE_ITEMS) from exception

def __recursive_quicksort(items: list, start_idx, end_idx):

    if start_idx >= len(items) or end_idx <= 0:
        return

    pivot = items[start_idx]

    left_index = start_idx + 1
    right_index = end_idx

    while left_index < right_index:
        while left_index < len(items) and items[left_index] < pivot:
            left_index = left_index + 1
        while right_index > 0 and pivot < items[right_index]:
            right_index = right_index - 1
        if left_index < right_index and items[right_index] < items[left_index]:
            items[left_index], items[right_index] = items[right_index], items[left_index]
            left_index = left_index + 1
            right_index = right_index - 1
    if start_idx < right_index and items[right_index] < items[start_idx]:
            items[start_idx], items[right_index] = items[right_index], items[start_idx]
    __recursive_quicksort(items, start_idx, right_index-1)
    __recursive_quicksort(items, left_index, len(items) - 1)

def main():
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print("Пример рекурсивной быстрой сортировки")
    print(f"Исходный список: {items}")
    recursive_quicksort(items)
    print(f"Отсортированный список: {items}")

if __name__ == "__main__":
    main()
