def _check_int(value, name):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Параметр {name} не является целым числом")

def _any(n, s, out):
    if n == 0:
        out.append(s)
    else:
        _any(n-1, s + "1", out)
        _after_zero (n-1, s + "0", out)

def _after_zero(n, s, out):
    if n == 0:
        out.append(s)
    else:
        _any(n-1, s + "1", out)

def grnerate_strings(length: int) -> list[str]:
    _check_int(length, "length")
    if length < 1:
        raise ValueError("Длина строки меньше единицы")
    out = []
    _any(length, "", out)
    return out

def _check_nk(n, k):
    _check_int(n, "n")
    _check_int(k, "k")
    if n < 0 or k < 0:
        raise ValueError("Параметры должны быть неотрицательными")
    if n < k:
        raise ValueError("Параметр n меньше k")

def binomial_coefficient_iter(n: int, k: int) -> int:
    _check_nk(n, k)
    row = [1]
    for _ in range(n):
        row = [1, *(a + b for a, b in zip(row, row[1:])), 1]
    return row[k]

def binomial_coefficient_rec(n: int, k: int) -> int:
    _check_nk(n, k)
    return _rec(n, k)

def _rec(n, k):
    if k == 0 or k == n:
        return 1
    return _rec(n - 1, k) + _rec(n - 1, k - 1)

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
