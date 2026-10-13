LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    validation(length=length)

    if length == 1:
            return ["0", "1"]
    
    strings = ["1" + string for string in generate_strings(length - 1)]
    strings += ["0" + string for string in _generate_after_zero(length - 1)]
    return strings
    
def _generate_after_zero(length: int) -> list[str]:
    """Возвращает допустимые продолжения строки после символа 0."""
    if length == 1:
        return ["1"]
    
    return ["1" + string for string in generate_strings(length - 1)]


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validation(n=n, k=k)
    k = min(k, n - k)

    row = [1]
    for current_n in range(1, n + 1):
        new_row = [1] * (current_n + 1)
        for current_k in range(1, current_n):
            new_row[current_k] = row[current_k - 1] + row[current_k]
        row = new_row

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
    validation(n=n, k=k)

    return recursion(n, k, {})

def recursion (n, k, memmory):
    if k == 0 or k == n:
        return 1
    if (n, k) not in memmory:
        memmory[n, k] = recursion(n - 1, k - 1, memmory) + recursion (n - 1, k, memmory)

    return memmory[n, k]


def validation(length = None, n = None, k = None):
    if length is not None:
        if isinstance(length, bool) or not isinstance(length, int):
            raise TypeError(LENGTH_NOT_INT)
        if length < 1:
            raise ValueError(LENGTH_NOT_POS)

    if n is not None or k is not None:
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))
        if isinstance(k, bool) or not isinstance(k, int):
            raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))
        if n < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
        if k < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
        if n < k:
            raise ValueError(N_LESS_THAN_K_ERROR_MSG)
    


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
