from collections.abc import Generator


def generate_permutations(elements: list) -> Generator[list, None, None]:
    """Выдаёт все перестановки элементов списка по одной.

    Каждая следующая получается из предыдущей. Рекурсия не используется.
    Порядок выдачи лексикографический. Повторы и пропуски недопустимы.

    :param elements: список любых сравнимых элементов
    :raises TypeError: аргумент не является списком
    :return: генератор перестановок; для пустого списка — одна пустая
        перестановка
    """
    if not isinstance(elements, list):
        raise TypeError("Аргумент elements должен быть списком")

    def permutations() -> Generator[list, None, None]:
        current = sorted(elements)
        while True:
            yield current.copy()

            pivot = len(current) - 2
            while pivot >= 0 and not current[pivot] < current[pivot + 1]:
                pivot -= 1
            if pivot < 0:
                return

            successor = len(current) - 1
            while not current[pivot] < current[successor]:
                successor -= 1
            current[pivot], current[successor] = current[successor], current[pivot]

            current[pivot + 1 :] = reversed(current[pivot + 1 :])

    return permutations()
