def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель разложением по строке.

    :param matrix: квадратная целочисленная матрица порядка не меньше 1
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    if not isinstance(matrix, list):
        raise TypeError("Матрица должна быть списком строк")
    if not matrix:
        raise ValueError("Порядок матрицы должен быть не меньше 1")

    order = len(matrix)
    for row in matrix:
        if not isinstance(row, list):
            raise TypeError("Каждая строка матрицы должна быть списком")
        if len(row) != order:
            raise ValueError("Матрица должна быть квадратной")
        if any(not isinstance(value, int) or isinstance(value, bool) for value in row):
            raise TypeError("Элементы матрицы должны быть целыми числами")

    return _expand_by_row(matrix)


def _expand_by_row(matrix: list[list[int]]) -> int:
    """Раскладывает определитель проверенной матрицы по первой строке."""
    if len(matrix) == 1:
        return matrix[0][0]

    determinant = 0
    for column, value in enumerate(matrix[0]):
        if value == 0:
            continue
        minor = [row[:column] + row[column + 1 :] for row in matrix[1:]]
        determinant += (-1) ** column * value * _expand_by_row(minor)
    return determinant


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
