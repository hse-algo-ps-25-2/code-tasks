from enum import StrEnum


class ErrorMessages(StrEnum):
    "Перечисление сообщений об ошибках"

    LENGTH_NOT_INT = "Длина строки не является целым числом"
    LENGTH_NOT_POS = "Длина строки меньше единицы"
    NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
    NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
    N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def __check_strings_generator_constraints(length: int) -> None:
    """Проверяет параметр генератора строк из 0 и 1 без двух 0 подряд длины length.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    """

    if not isinstance(length, int):
        raise TypeError(ErrorMessages.LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(ErrorMessages.LENGTH_NOT_POS)


def __generate_strings_with_prefix_not_ending_with_0(
    prefix: str, length: int
) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом, начинающиеся на заданний префикс, окончивающийся не на 0.

    :param prefix: строка префикс из 0 и 1 без двух нолей подряд окончивающаяся не на 0
    :param length: длина строки которую приписать к префиксу, целое число не меньше 1
    :return: список строк
    """

    if length == 1:
        return [prefix + "0", prefix + "1"]

    return __generate_strings_with_prefix_ending_with_0(
        prefix + "0", length - 1
    ) + __generate_strings_with_prefix_not_ending_with_0(prefix + "1", length - 1)


def __generate_strings_with_prefix_ending_with_0(prefix: str, length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом, начинающиеся на заданний префикс, окончивающийся не на 0.

    :param prefix: строка префикс из 0 и 1 без двух нолей подряд окончивающаяся не на 0
    :param length: длина строки которую приписать к префиксу, целое число не меньше 1
    :return: список строк
    """

    if length == 1:
        return [prefix + "1"]

    return __generate_strings_with_prefix_not_ending_with_0(prefix + "1", length - 1)


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    print(f"generate_strings length={length}")
    __check_strings_generator_constraints(length)
    return __generate_strings_with_prefix_not_ending_with_0("", length)


def __check_binominal_coefficient_constraints(n: int, k: int) -> None:
    """Проверяет параметры функции вычисления биномиального коэффициента из n по k.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    """

    if not isinstance(n, int):
        raise TypeError(ErrorMessages.NOT_INT_VALUE_TEMPL.format("n"))
    if not isinstance(k, int):
        raise TypeError(ErrorMessages.NOT_INT_VALUE_TEMPL.format("k"))

    if n < 0:
        raise ValueError(ErrorMessages.NEGATIVE_VALUE_TEMPL.format("n"))
    if k < 0:
        raise ValueError(ErrorMessages.NEGATIVE_VALUE_TEMPL.format("k"))

    if n < k:
        raise ValueError(ErrorMessages.N_LESS_THAN_K_ERROR_MSG)


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    __check_binominal_coefficient_constraints(n, k)

    if k == 0 or k == n:
        return 1

    row = [1]
    for i in range(1, n + 1, 1):
        prev_row = row
        row = [1] * i
        for j in range(1, i - 1):
            row[j] = prev_row[j - 1] + prev_row[j]
    return row[k - 1] + row[k]


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    __check_binominal_coefficient_constraints(n, k)

    if k == 0 or n == k:
        return 1
    return binomial_coefficient_rec(n - 1, k) + binomial_coefficient_rec(n - 1, k - 1)


def main():
    n = 2
    print(f"Строки длиной {n}:\n{generate_strings(n)}\n")

    n = 1
    print(f"Строки длиной {n}:\n{generate_strings(n)}\n")

    n = 3
    print(f"Строки длиной {n}:\n{generate_strings(n)}\n")

    n = 30
    k = 20
    print(
        f"Биномиальный коэффициент (итеративно) при n, k ({n}, {k}) = ",
        binomial_coefficient_iter(n, k),
    )
    n = 5
    k = 2
    print(
        f"Биномиальный коэффициент (рекурсивно) при n, k ({n}, {k}) = ",
        binomial_coefficient_rec(n, k),
    )


if __name__ == "__main__":
    main()
