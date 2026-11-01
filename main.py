from typing import Any


def _validate(elements: Any) -> None:
    """Проверяет, что значение является списком без дубликатов.

    :param elements: любое значение
    :raises TypeError: elements не является списком
    :raises ValueError: в списке есть дубликаты
    :return: None
    """
    if not isinstance(elements, list):
        raise TypeError("Аргумент не является списком.")
    for i, a in enumerate(elements):
        for b in elements[i + 1 :]:
            if type(a) is type(b) and a == b:
                raise ValueError("В списке есть дубликаты.")


def generate_permutations_rec(elements: list) -> list[list]:
    """Возвращает все перестановки элементов списка.

    Порядок перестановок в списке не фиксируется. Повторы и пропуски
    недопустимы.

    :param elements: список любых элементов
    :raises TypeError: аргумент не является списком
    :raises ValueError: в списке есть дубликаты
    :return: список перестановок; для пустого списка — список из одной
        пустой перестановки
    """
    _validate(elements)

    def _generate_permutations_rec(elements: list) -> list[list]:
        if len(elements) == 0:
            return [[]]

        *rest, new_element = elements
        t0 = _generate_permutations_rec(rest)

        result = []

        for permutation in t0:
            permutation.insert(0, new_element)
            result.append(permutation)

            prev_permutation = permutation
            for i in range(len(permutation) - 1):
                perm_copy = prev_permutation.copy()
                perm_copy[i], perm_copy[i + 1] = perm_copy[i + 1], perm_copy[i]
                result.append(perm_copy)
                prev_permutation = perm_copy

        return result

    return _generate_permutations_rec(elements)


def generate_permutations_iter(elements: list) -> list[list]:
    """Возвращает все перестановки элементов списка.

    Итеративная реализация, без рекурсии. Порядок перестановок
    в списке не фиксируется. Повторы и пропуски недопустимы.

    :param elements: список любых элементов
    :raises TypeError: аргумент не является списком
    :raises ValueError: в списке есть дубликаты
    :return: список перестановок; для пустого списка — список из одной
        пустой перестановки
    """
    _validate(elements)

    result = [[]]
    for cur_element in elements:
        new_result = []
        for cur_perm in result:
            for insert_idx in range(len(cur_perm) + 1):
                cur_perm_copy = cur_perm.copy()
                cur_perm_copy.insert(insert_idx, cur_element)
                new_result.append(cur_perm_copy)

        result = new_result

    return result


def main():
    for elements in ([], ["a"], ["a", "b", "c"]):
        print(f"{elements}, рекурсивно: {generate_permutations_rec(elements)}")
        print(f"{elements}, итеративно: {generate_permutations_iter(elements)}")


if __name__ == "__main__":
    main()
