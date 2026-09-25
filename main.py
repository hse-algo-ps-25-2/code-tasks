def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной матрицы разложением.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    n = len(matrix)

    # порядок меньше 1 или не квадратная
    if n == 0 or any(len(row) != n for row in matrix):
        raise Exception()
    # в каждой диагонали, кроме трёх, должны быть 0 - проверяем первую строку и первый столбец
    if any(x != 0 for x in matrix[0][2:]) or any(row[0] != 0 for row in matrix[2:]):
        raise Exception()

    res = 0
    res += matrix[0][0] * (1 if n == 1 else get_tridiagonal_determinant([row[1:] for row in matrix[1:]]))
    if n > 1:
        res -= matrix[0][1] * matrix[1][0] * (1 if n < 3 else get_tridiagonal_determinant([row[2:] for row in matrix[2:]]))

    return res


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
