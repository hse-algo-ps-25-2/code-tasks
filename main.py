from functools import cache

LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def generate_strings(length: int) -> list[str]:
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)

    def ends_with_one(n):
        if n == 1:
            return {"1"}
        return {s + "1" for s in ends_with_one(n - 1) | ends_with_zero(n - 1)}

    def ends_with_zero(n):
        if n == 1:
            return {"0"}
        return {s + "0" for s in ends_with_one(n - 1)}

    return list(ends_with_one(length) | ends_with_zero(length))


def check_binomial_args(n, k):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def binomial_coefficient_iter(n: int, k: int) -> int:
    check_binomial_args(n, k)

    row = [1]
    for i in range(1, n + 1):
        next_row = [1] * (i + 1)
        for j in range(1, i):
            next_row[j] = row[j - 1] + row[j]
        row = next_row
    return row[k]


def binomial_coefficient_rec(n: int, k: int) -> int:
    check_binomial_args(n, k)

    @cache
    def calculate(a, b):
        if b == 0 or b == a:
            return 1
        return calculate(a - 1, b) + calculate(a - 1, b - 1)

    return calculate(n, k)


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
