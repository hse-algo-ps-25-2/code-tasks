def generate_permutations_rec(elements: list) -> list[list]:
    """Возвращает все перестановки элементов списка.

    Порядок перестановок в списке не фиксируется. Повторы и пропуски
    недопустимы.

    :param elements: список любых элементов
    :raises TypeError: аргумент не является списком
    :return: список перестановок; для пустого списка — список из одной
        пустой перестановки
    """
    pass


def generate_permutations_iter(elements: list) -> list[list]:
    """Возвращает все перестановки элементов списка.

    Итеративная реализация, без рекурсии. Порядок перестановок
    в списке не фиксируется. Повторы и пропуски недопустимы.

    :param elements: список любых элементов
    :raises TypeError: аргумент не является списком
    :return: список перестановок; для пустого списка — список из одной
        пустой перестановки
    """
    if not isinstance(elements, list):
        raise TypeError("Аргумент не является списком.")

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
