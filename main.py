def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной матрицы разложением.

    :param matrix: Квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """

    check_matrix(matrix)

    lm = len(matrix)
    if lm == 1:
        return matrix[0][0]

    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    cache = {0: 1, 1: a}

    return det(lm, a, b, c, cache)


def det(k: int, a: int, b: int, c: int, cache: dict[int, int]) -> int:
    if k in cache.keys():
        return cache[k]
    cache[k] = a * det(k - 1, a, b, c, cache) - b * c * det(k - 2, a, b, c, cache)
    return cache[k]


def check_matrix(matrix: list[list[int]]):
    lm = len(matrix)
    a = matrix[0][0]

    if not isinstance(matrix, list) or not matrix:
        raise Exception("Матрица пустая или None")

    for row in range(lm):
        if not isinstance(matrix[row], list) or len(matrix[row]) != lm:
            raise Exception("Матрица должна быть квадратной")

        for column in range(lm):
            elem = matrix[row][column]
            if not isinstance(elem, int) or isinstance(elem, bool):
                raise Exception("Все элементы должны быть целыми числами")
            elif abs(row - column) > 1 and elem != 0:
                raise Exception("Все элементы вне диагонали должны быть равны 0")
            elif row == column and elem != a:
                raise Exception("Главная диагональ должна быть постоянной")
            elif row > 0 and column == row - 1 and elem != matrix[1][0]:
                raise Exception("Нижняя диагональ должна быть постоянной")
            elif row < lm - 1 and column == row + 1 and elem != matrix[0][1]:
                raise Exception("Верхняя диагональ должна быть постоянной")


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
