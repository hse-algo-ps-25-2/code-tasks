LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _any(n, s, out):
    if n == 0:
        out.append(s)
    else:
        _any(n - 1, s + "1", out)
        _after_zero(n - 1, s + "0", out)


def _after_zero(n, s, out):
    if n == 0:
        out.append(s)
    else:
        _any(n - 1, s + "1", out)


def generate_strings(length: int) -> list[str]:
    if not _is_int(length):
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)
    out = []
    _any(length, "", out)
    return out


def _check_nk(n, k):
    for value, name in ((n, "n"), (k, "k")):
        if not _is_int(value):
            raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
        if value < 0:
            raise TypeError(NEGATIVE_VALUE_TEMPL.format(name))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def binomial_coefficient_iter(n: int, k: int) -> int:
    _check_nk(n, k)
    row = [1]
    for _ in range(n):
        row = [1, *(a + b for a, b in zip(row, row[1:])), 1]
    return row[k]


def _rec(n, k):
    if k == 0 or k == n:
        return 1
    return _rec(n - 1, k) + _rec(n - 1, k - 1)


def binomial_coefficient_rec(n: int, k: int) -> int:
    _check_nk(n, k)
    return _rec(n, k)


def main():
    print(generate_strings(2))
    print(binomial_coefficient_iter(30, 20))
    print(binomial_coefficient_rec(5, 2))


if __name__ == "__main__":
    main()
