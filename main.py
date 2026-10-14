PATH_LENGTH_NOT_INT = "Длина маршрута не является целым числом"
PATH_LENGTH_NOT_POS = "Длина маршрута меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"

triangle_path_cache_a = {}
triangle_path_cache_b = {}
triangle_path_cache_c = {}


def get_triangle_path_count_a(length: int) -> int:
    """
    Возвращает число маршрутов заданной длины
    из вершины A в вершину A треугольника ABC

    :param length: длина маршрута, целое число не меньше 1
    """
    if length == 1:
        return 0
    if triangle_path_cache_a.get(length) is not None:
        return triangle_path_cache_a[length]
    result = get_triangle_path_count_b(length - 1) + get_triangle_path_count_c(
        length - 1
    )
    triangle_path_cache_a[length] = result
    return result


def get_triangle_path_count_b(length: int) -> int:
    """
    Возвращает число маршрутов заданной длины
    из вершины A в вершину B треугольника ABC

    :param length: длина маршрута, целое число не меньше 1
    """
    if length == 1:
        return 1
    if triangle_path_cache_b.get(length) is not None:
        return triangle_path_cache_b[length]
    result = get_triangle_path_count_a(length - 1) + get_triangle_path_count_c(
        length - 1
    )
    triangle_path_cache_b[length] = result
    return result


def get_triangle_path_count_c(length: int) -> int:
    """
    Возвращает число маршрутов заданной длины
    из вершины A в вершину C треугольника ABC

    :param length: длина маршрута, целое число не меньше 1
    """
    if length == 1:
        return 1
    if triangle_path_cache_c.get(length) is not None:
        return triangle_path_cache_c[length]
    result = get_triangle_path_count_a(length - 1) + get_triangle_path_count_b(
        length - 1
    )
    triangle_path_cache_c[length] = result
    return result


def get_triangle_path_count(length: int) -> int:
    """Возвращает число замкнутых маршрутов заданной длины
    из вершины A в вершину A треугольника ABC.

    :param length: длина маршрута, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: число маршрутов
    """
    if not isinstance(length, int):
        raise TypeError(PATH_LENGTH_NOT_INT)
    if isinstance(length, bool):
        raise TypeError(PATH_LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(PATH_LENGTH_NOT_POS)
    return get_triangle_path_count_a(length)


def _validate_binomial_coefficient(n: int, k: int) -> None:
    if type(n) is not int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))
    if type(k) is not int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
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
    _validate_binomial_coefficient(n, k)

    binomial_coefficient = 1

    for i in range(1, k + 1):
        binomial_coefficient = binomial_coefficient * (n - k + i) // i

    return binomial_coefficient


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по соотношению C(n, k) = (n / k) * C(n - 1, k - 1).

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial_coefficient(n, k)

    def _binomial_coefficient_rec(n: int, k: int) -> int:
        """Внутренняя рекурсивная функция без повторной валидации."""
        if k == 0 or k == n:
            return 1

        return n * _binomial_coefficient_rec(n - 1, k - 1) // k

    return _binomial_coefficient_rec(n, k)


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
