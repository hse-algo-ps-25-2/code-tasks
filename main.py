LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _validate_binomial_args(n: int, k: int) -> None:
    for name, value in (("n", n), ("k", k)):
        if type(value) is not int:
            raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
        if value < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def _after_zero(current: str, length: int, result: list[str]) -> None:
    if len(current) == length:
        result.append(current)
        return
    _after_one(current + "1", length, result)


def _after_one(current: str, length: int, result: list[str]) -> None:
    if len(current) == length:
        result.append(current)
        return
    _after_zero(current + "0", length, result)
    _after_one(current + "1", length, result)


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    if type(length) is not int:
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)
    result = []
    _after_one("", length, result)
    return result


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial_args(n, k)
    row = [1] + [0] * k
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):
            row[j] += row[j - 1]
    return row[k]


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial_args(n, k)

    def pascal(n: int, k: int) -> int:
        if k == 0 or k == n:
            return 1
        return pascal(n - 1, k - 1) + pascal(n - 1, k)

    return pascal(n, k)


def main():
    n = 2
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
