LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _put_one(result_arr, remaining, prefix):
    if remaining == 0:
        result_arr.append(prefix)
    else:
        _put_both(result_arr, remaining - 1, prefix + "1")


def _put_both(arr, length, s=""):
    if length == 0:
        arr.append(s)
    else:
        _put_both(arr, length - 1, s + "1")
        _put_one(
            arr,
            length - 1,
            s + "0",
        )


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)

    strings = []

    _put_both(strings, length)

    return strings


def _validate_param(value, name):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
    if value < 0:
        raise TypeError(NEGATIVE_VALUE_TEMPL.format(name))


def _handle_raise(n, k):
    _validate_param(n, "n")
    _validate_param(k, "k")
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _handle_raise(n, k)

    triangle = [[1]]

    for row_idx in range(1, n + 1):
        prev_row = triangle[row_idx - 1]
        internal_part_of_row = []

        for j in range(1, row_idx):
            internal_part_of_row.append(prev_row[j - 1] + prev_row[j])

        full_row = [1] + internal_part_of_row + [1]

        triangle.append(full_row)

    return triangle[n][k]


def _solve_with_rec(n: int, k: int) -> int:
    if (k == 0) or (n == k) or (n == 0 and k == 0):
        return 1
    else:
        return _solve_with_rec(n - 1, k) + _solve_with_rec(n - 1, k - 1)


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _handle_raise(n, k)

    return _solve_with_rec(n, k)


def main():
    n = 4
    print(f"Строки длиной {n}:\n{generate_strings(n)}")

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
