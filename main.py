def validate_matrix(matrix: list[list[int]]) -> None:
    if not isinstance(matrix, list):
        raise Exception("Некорректный тип входных данных")

    if len(matrix) == 0:
        raise Exception("Матрица не должна быть пустой")

    row_counts = len(matrix)

    for row in matrix:
        if not isinstance(row, list):
            raise Exception("Некорректный тип строки матрицы")
        columns_count = len(row)
        if columns_count != row_counts:
            raise Exception("Матрица должны быть квадратной")

        for value in row:
            if type(value) is not int:
                raise Exception("Элементы матрица должны быть целочисленными")


def calculate_determinant_rec(matrix: list[list[int]]) -> int:
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    row = matrix[0]
    det = 0

    for idx, value in enumerate(row):
        minor_matrix = [cur_row[:idx] + cur_row[idx + 1 :] for cur_row in matrix[1:]]
        minor = calculate_determinant_rec(minor_matrix)
        det += value * (-1) ** (idx) * minor

    return det


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель разложением по строке.

    :param matrix: квадратная целочисленная матрица порядка не меньше 1
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    validate_matrix(matrix)

    return calculate_determinant_rec(matrix)


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
