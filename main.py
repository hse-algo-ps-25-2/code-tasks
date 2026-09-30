def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель разложением по строке.

    :param matrix: квадратная целочисленная матрица порядка не меньше 1
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    n = len(matrix)

    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("Матрица должна быть непустой и квадратной")

    for row in matrix:
        for value in row:
            if type(value) is not int:
                raise TypeError("Элементы матрицы должны быть целыми числами")

    def determinant(m):
        if len(m) == 1:
            return m[0][0]

        result = 0

        for j in range(len(m)):
            minor = [row[:j] + row[j + 1:] for row in m[1:]]
            result += (-1) ** j * m[0][j] * determinant(minor)

        return result

    return determinant(matrix)


def main():
    matrix = [[1, 2], [3, 4]]
    print(calculate_determinant(matrix))


if __name__ == "__main__":
    main()