PATH_LENGTH_NOT_INT = "Длина маршрута не является целым числом"
PATH_LENGTH_NOT_POS = "Длина маршрута меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def get_triangle_path_count(length: int) -> int:
    """Возвращает число замкнутых маршрутов заданной длины
    из вершины A в вершину A треугольника ABC.

    :param length: длина маршрута, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: число маршрутов
    """
    pass


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    if type(n) != int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))
    if type(k) != int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))

    if k < 1:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    if n < 1:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)

    c_n_k = 1
    for i in range(1, k+1):
        c_n_k = c_n_k * (n - k + i) // i
    return c_n_k


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по соотношению C(n, k) = (n / k) * C(n - 1, k - 1).

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    if type(n) != int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))
    if type(k) != int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))

    if k < 1:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    if n < 1:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)

    if k == 1:
        return n

    return binomial_coefficient_rec(n - 1, k - 1) * n // k


def main():
    n = 4
    print(f"Количество маршрутов длиной {n} = {get_triangle_path_count(n)}")

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
