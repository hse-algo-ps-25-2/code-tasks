import typing


def validate_matrix(matrix: typing.Any) -> None:
    """Проверяет, что значение является квадратной целочисленной матрицей
    порядка не меньше 1.

    :param matrix: любое значение
    :raises Exception: если matrix не является такой матрицей
    :return: None
    """
    if not isinstance(matrix, list):
        raise Exception("Матрица должна быть типа list")
    if len(matrix) < 1:
        raise Exception("Матрица должна быть порядка не меньше 1")
    if not all(isinstance(row, list) for row in matrix):
        raise Exception("Все строки матрицы должны быть типа list")
    if any(len(row) != len(matrix) for row in matrix):
        raise Exception("Матрица должна быть квадратной")
    if not all(type(item) is int for row in matrix for item in row):
        raise Exception("Матрица должна быть целочисленной")


def truncate_matrix(matrix: list[list[int]], deleted_col_idx: int) -> list[list[int]]:
    """Строит новую матрицу, удаляя из исходной строку с индексом 0
    и столбец с индексом deleted_col_idx.

    :param matrix: исходная матрица
    :param deleted_col_idx: индекс удаляемого столбца
    :return: матрица порядка на 1 меньше
    """
    truncated_matrix = []

    for _ in range(len(matrix) - 1):
        truncated_matrix.append([])

    for row_idx in range(1, len(matrix)):
        for col_idx in range(len(matrix)):
            if col_idx != deleted_col_idx:
                truncated_matrix[row_idx - 1].append(matrix[row_idx][col_idx])

    return truncated_matrix


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель разложением по строке.

    :param matrix: квадратная целочисленная матрица порядка не меньше 1
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    validate_matrix(matrix)

    def calc_det(matrix: list[list[int]]) -> int:
        # база рекурсии: определитель матрицы 1x1 равен единственному элементу
        if len(matrix) == 1:
            return matrix[0][0]

        # определитель вычисляется разложением по первой строке
        ROW_IDX = 0
        determinant = 0

        for col_idx in range(len(matrix[ROW_IDX])):
            item = matrix[ROW_IDX][col_idx]
            minor = calc_det(truncate_matrix(matrix, col_idx))
            # алгебраическое дополнение
            cofactor = pow(-1, ROW_IDX + col_idx) * minor
            determinant += item * cofactor

        return determinant

    return calc_det(matrix)


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
