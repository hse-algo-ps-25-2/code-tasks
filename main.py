LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _validate_length_param(length: int) -> None:
    """Проводит валидацию параметра **length**.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    """
    if not isinstance(length, int):
        raise TypeError(LENGTH_NOT_INT)

    if length < 1:
        raise ValueError(LENGTH_NOT_POS)


def _validate_n_and_k_params(n: int, k: int) -> None:
    """Проводит валидацию параметров **n** и **k**.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    """
    if not isinstance(n, int):
        raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))

    if not isinstance(k, int):
        raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))

    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))

    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))

    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def _generate_zero_ending_strings(length: int) -> list[str]:
    """Возвращает строки с нулём на конце, исключая строки c двумя нулями подряд."""
    if length == 1:
        return ["0"]

    return [s + "0" for s in _generate_one_ending_strings(length - 1)]


def _generate_one_ending_strings(length: int) -> list[str]:
    """Возвращает строки с единицей на конце."""
    if length == 1:
        return ["1"]

    return [
        s + "1"
        for s in _generate_zero_ending_strings(length - 1)
        + _generate_one_ending_strings(length - 1)
    ]


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    Использует функции **_generate_zero_ending_strings()**
    и **_generate_one_ending_strings()**

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    _validate_length_param(length)

    return _generate_zero_ending_strings(length) + _generate_one_ending_strings(length)


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_n_and_k_params(n, k)

    k = min(k, n - k)

    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_n_and_k_params(n, k)


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
