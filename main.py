LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _is_int(value) -> bool:
    """Проверяет, что значение является целым числом.

    bool не считается целым, хотя в Python является подклассом int.

    :param value: проверяемое значение
    :return: True, если значение целое и не bool
    """
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_length(length: int) -> None:
    """Проверяет длину строки для generate_strings.

    :param length: длина строки
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    """
    if not _is_int(length):
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)


def _validate_binomial_args(n: int, k: int) -> None:
    """Проверяет аргументы биномиального коэффициента.

    Общая проверка для итеративной и рекурсивной функций, поэтому
    обе функции реагируют на некорректный вход одинаково.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    """
    for name, value in (("n", n), ("k", k)):
        if not _is_int(value):
            raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
    for name, value in (("n", n), ("k", k)):
        if value < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def _append_any_symbol(prefix: str, remaining: int, result: list[str]) -> None:
    """Достраивает строку, которая пуста или оканчивается на '1'.

    Следующим символом может быть как '0', так и '1'.

    :param prefix: уже построенная часть строки
    :param remaining: сколько символов осталось дописать
    :param result: список, в который добавляются готовые строки
    """
    if remaining == 0:
        result.append(prefix)
        return
    _append_after_zero(prefix + "0", remaining - 1, result)
    _append_any_symbol(prefix + "1", remaining - 1, result)


def _append_after_zero(prefix: str, remaining: int, result: list[str]) -> None:
    """Достраивает строку, которая оканчивается на '0'.

    Следующим символом может быть только '1'.

    :param prefix: уже построенная часть строки
    :param remaining: сколько символов осталось дописать
    :param result: список, в который добавляются готовые строки
    """
    if remaining == 0:
        result.append(prefix)
        return
    _append_any_symbol(prefix + "1", remaining - 1, result)


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    _validate_length(length)
    result: list[str] = []
    _append_any_symbol("", length, result)
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

    # pascal_row[position] = C(row_number, position).
    # Обновление справа налево: C(r, p) = C(r - 1, p) + C(r - 1, p - 1).
    pascal_row = [1] + [0] * k
    for row_number in range(1, n + 1):
        for position in range(min(row_number, k), 0, -1):
            pascal_row[position] += pascal_row[position - 1]
    return pascal_row[k]


def _binomial_pascal_cached(n: int, k: int, cache: dict[tuple[int, int], int]) -> int:
    """Рекурсивно вычисляет C(n, k) по правилу Паскаля с кешированием.

    C(n, k) = C(n - 1, k) + C(n - 1, k - 1), C(n, 0) = C(n, n) = 1.
    Аргументы считаются уже проверенными.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :param cache: словарь уже вычисленных значений по ключу (n, k)
    :return: значение биномиального коэффициента
    """
    if k == 0 or k == n:
        return 1
    if (n, k) not in cache:
        cache[(n, k)] = _binomial_pascal_cached(
            n - 1, k, cache
        ) + _binomial_pascal_cached(n - 1, k - 1, cache)
    return cache[(n, k)]


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
    return _binomial_pascal_cached(n, k, {})


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
