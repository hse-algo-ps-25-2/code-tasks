def check_validation_matrix(matrix: list[list[int]]) -> None:
    """Проверка матрицы на корректность."""
    if not isinstance(matrix, list):
        raise Exception("Матрица должна быть словарём.")

    len_matrix = len(matrix)

    if len_matrix == 0 or matrix is None:
        raise Exception("Матрица не должна быть пустой.")

    for row in matrix:
        if not isinstance(row, list):
            raise Exception("Матрица должна состоять из словарей.")
        
        if len(row) != len_matrix:
            raise Exception("Матрица должна быть квадратной.")

        for value in row:
            if not isinstance(value, int):
                raise Exception("Элементы матрицы должны быть целыми числами.")


def check_matrix_values(
    matrix: list[list[int]],
    a: int,
    b: int, 
    c: int,
) -> None:
    """Проверка диагоналей матрицы."""
    len_matrix = len(matrix)

    for i in range(len_matrix):
        for j in range(len_matrix):
            if i == j:
                if matrix[i][j] != a:
                    raise Exception("Значения на главной диагонали должны быть одинаковыми.")
            elif j == i + 1:
                if matrix[i][j] != b:
                    raise Exception("Значения на наддиагонали должны быть одинаковыми.")
            elif i == j + 1:
                if matrix[i][j] != c:
                    raise Exception("Значения на поддиагонали должны быть одинаковыми.")
            elif matrix[i][j] != 0:
                raise Exception("Вне трёх диагоналей должны находиться только нули.")


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Итеративное вычисление определителя трёхдиагональной матрицы.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    check_validation_matrix(matrix)

    len_matrix = len(matrix)
    if len_matrix == 1:
        return matrix[0][0]
    
    a, b, c = matrix[0][0], matrix[0][1], matrix[1][0]
    
    check_matrix_values(matrix, a, b, c)

    determinant_before_previous = 1
    determinant_previous = a

    for _ in range(2, len_matrix + 1):
        determinant = a * determinant_previous - b * c * determinant_before_previous
        determinant_before_previous = determinant_previous
        determinant_previous = determinant

    return determinant_previous


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
