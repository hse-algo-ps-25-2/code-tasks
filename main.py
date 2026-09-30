def validate_matrix_structure(matrix: list[list[int]]) -> None:
    if type(matrix) is not list:
        raise ValueError("Incorrect matrix")

    if not matrix:
        raise ValueError("Incorrect matrix")

    for row in matrix:
        if type(row) is not list:
            raise ValueError("Incorrect matrix")
        if len(row) != len(matrix):
            raise ValueError("Non square matrix")

        for value in row:
            if type(value) is not int:
                raise ValueError("Non int matrix")


def validate_tridiagonal_matrix(matrix: list[list[int]]) -> None:
    n = len(matrix)
    a = matrix[0][0]
    b = matrix[0][1] if n > 1 else 1
    c = matrix[1][0] if n > 1 else 1

    for i in range(n):
        for j in range(n):
            if i == j:
                expected = a
            elif i + 1 == j:
                expected = b
            elif i == j + 1:
                expected = c
            else:
                expected = 0

            if matrix[i][j] != expected:
                raise ValueError("Not a tridiagonal matrix")


def validate_matrix(matrix: list[list[int]]) -> None:
    validate_matrix_structure(matrix)
    validate_tridiagonal_matrix(matrix)


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    validate_matrix(matrix)

    n = len(matrix)
    a = matrix[0][0]
    b = matrix[0][1] if n > 1 else 1
    c = matrix[1][0] if n > 1 else 1

    previous_previous = 1
    previous = a

    for i in range(2, n + 1):
        current = a * previous - b * c * previous_previous
        previous_previous = previous
        previous = current

    return previous


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
