from typing import Any

from constants import Exceptions


def _merge(left: list[Any], right: list[Any]) -> list[Any]:
    """
    Сливает два отсортированных списка в один отсортированный. Вспомогательная функция для recursive_sort.

    :param left: отсортированный список сравниваемых элементов
    :param right: отсортированный список сравниваемых элементов
    :raise TypeError: если элементы несравниваемы
    :return: новый отсортированный список из элементов left и right.
    """
    left_cursor = right_cursor = 0
    result = []
    try:
        while left_cursor < len(left) and right_cursor < len(right):
            if left[left_cursor] < right[right_cursor]:
                result.append(left[left_cursor])
                left_cursor += 1
            else:
                result.append(right[right_cursor])
                right_cursor += 1
    except TypeError as exc:
        raise TypeError(Exceptions.NOT_COMPARABLE) from exc
    result.extend(left[left_cursor:])
    result.extend(right[right_cursor:])
    return result


def _sort(items: list[Any]) -> list[Any]:
    """
    Рекурсивно сортирует список слиянием. Вспомогательная функция для recursive_sort.

    :param items: список сравниваемых элементов
    :return: новый отсортированный список
    """
    if len(items) <= 1:
        return items[:]

    mid_index = len(items) // 2
    left = _sort(items[:mid_index])
    right = _sort(items[mid_index:])
    return _merge(left, right)


def recursive_sort(items: list[Any]) -> list[Any]:
    """Возвращает новый список, упорядоченный по неубыванию.

    Алгоритм — merge sort.
    Элементы должны быть попарно сравнимы операцией <.

    :param items: список сравнимых элементов
    :raise TypeError: если items не список либо элементы несравнимы
    :return: новый отсортированный список
    """
    if not isinstance(items, list):
        raise TypeError(Exceptions.NOT_LIST)

    return _sort(items)


def main() -> None:
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print("Пример рекурсивной сортировки")
    print(f"Исходный список: {items}")
    print(f"Отсортированный список: {recursive_sort(items)}")


if __name__ == "__main__":
    main()
