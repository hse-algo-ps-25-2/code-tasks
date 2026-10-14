PATH_LENGTH_NOT_INT = "Длина маршрута не является целым числом"
PATH_LENGTH_NOT_POS = "Длина маршрута меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def a(m: int):
    if m == 0:
        return 1
    return b(m - 1) + c(m - 1)

def b(m: int):
    if m == 0:
        return 0
    return a(m - 1) + c(m - 1)

def c(m: int):
    if m == 0:
        return 0
    return a(m - 1) + b(m - 1)

def _validate_length(length: int) -> None:
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError(PATH_LENGTH_NOT_INT)

    if length < 1:
        raise ValueError(PATH_LENGTH_NOT_POS)


def _validate_n_k(n: int, k: int) -> None:
    for name, value in (("n", n), ("k", k)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(NOT_INT_VALUE_TEMPL.format(name))

    for name, value in (("n", n), ("k", k)):
        if value < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))

    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def get_triangle_path_count(length: int) -> int:
    _validate_length(length)

    return a(length)


def binomial_coefficient_iter(n: int, k: int) -> int:
    result = 1

    _validate_n_k(n, k)



    for i in range(1, k + 1):
        result = result * (n - k + i) // i

    return result


def binomial_coefficient_rec(n: int, k: int) -> int:
    _validate_n_k(n, k)

    def calculate(current_n: int, current_k: int) -> int:
        if current_k == 0:
            return 1

        return (
            current_n
            * calculate(current_n - 1, current_k - 1)
            // current_k
        )

    return calculate(n, k)


def main():
    n = 5
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
