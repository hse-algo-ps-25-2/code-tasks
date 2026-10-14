LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"

# Вариант 1.
#  Строки из 0 и 1 без двух нулей подряд (две процедуры со взаимной рекурсией)
# и биномиальный коэффициент по правилу Паскаля.

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
    generate_after_one("", length, result)

    return result


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validate_binomial_parameters(n, k)

    previous_row = [1]

    for row_number in range(1, n + 1):
        current_row = [1] * (row_number + 1)

        for column_number in range(1, row_number):
            current_row[column_number] = (
                previous_row[column_number - 1]
                + previous_row[column_number]
            )

        previous_row = current_row

    return previous_row[k]


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validate_binomial_parameters(n, k)
    return calculate_binomial_rec(n, k)

def calculate_binomial_rec(n: int, k: int) -> int:
    if k == 0 or k == n:
        return 1

    return (
        calculate_binomial_rec(n - 1, k - 1)
        + calculate_binomial_rec(n - 1, k)
    )

def validate_binomial_parameters(n: int, k: int) -> None:
    for parameter_name, parameter_value in (("n", n), ("k", k)):
        if type(parameter_value) is not int:
            raise TypeError(NOT_INT_VALUE_TEMPL.format(parameter_name))

        if parameter_value < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format(parameter_name))

    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def generate_after_zero(
    current_string: str,
    target_length: int,
    result: list[str],
) -> None:
    if len(current_string) == target_length:
        result.append(current_string)
        return

    generate_after_one(current_string + "1", target_length, result)


def generate_after_one(
    current_string: str,
    target_length: int,
    result: list[str],
) -> None:
    if len(current_string) == target_length:
        result.append(current_string)
        return

    generate_after_zero(current_string + "0", target_length, result)
    generate_after_one(current_string + "1", target_length, result)

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
