import random

NOT_LIST_ERROR_MESSAGE = "Набор не является списком"


def __check_constrains(items: list):
    "Проверка условий"

    if not isinstance(items, list):
        raise TypeError(NOT_LIST_ERROR_MESSAGE)


def recursive_quicksort(items: list) -> list:
    """Возвращает новый список, упорядоченный по неубыванию.
    Алгоритм — Быстрая сортировка (QuickSort).

    :param items: список сравнимых элементов.\
        Элементы должны быть попарно сравнимы операцией <.
    :raise TypeError: если items не список либо элементы несравнимы
    :return: новый отсортированный список
    """
    __check_constrains(items)
    return __recursive_quicksort(items)


def __recursive_quicksort(items: list) -> list:

    if len(items) <= 1:
        return items
    pivot = random.choice(items)
    less_than_pivot_items = [item for item in items if item < pivot]
    equal_pivot_items = [item for item in items if item == pivot]
    larger_than_pivot_items = [item for item in items if item > pivot]

    return (
        recursive_quicksort(less_than_pivot_items)
        + equal_pivot_items
        + recursive_quicksort(larger_than_pivot_items)
    )


def main():
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print("Пример рекурсивной быстрой сортировки")
    print(f"Исходный список: {items}")
    print(f"Отсортированный список: {recursive_quicksort(items)}")


if __name__ == "__main__":
    main()
