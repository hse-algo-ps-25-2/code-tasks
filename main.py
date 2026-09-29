def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:

    # zero check

    if not matrix:
        raise Exception("empty matrix")

    n = len(matrix)

    # squre check

    for row in matrix:
        if len(row) != n:
            raise Exception("Not square")

        for element in row:
            # int check
            if not isinstance(element, int):
                raise Exception("Not int value")

    if n == 1:
        return matrix[0][0]
    
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]

    # diagonal check

    for i in range(n):
        for j in range(n):
            if i == j:
                if matrix[i][j] != a:
                    raise Exception("not stable main diagonal")

            elif j == i + 1:
                if matrix[i][j] != b:
                    raise Exception("not stable up-diagonal")

            elif i == j + 1:
                if matrix[i][j] != c:
                    raise Exception("not stable down-diagonal")

            elif matrix[i][j] != 0:
                raise Exception("not 3 diagonal matrix")

    # D1 = a
    det_1 = a

    # D2 = a^2 - bc
    det_2 = a * a - b * c

    # Dn = a * D(n-1) - bc * D(n-2)
    for _ in range(3, n + 1):
        determinant = (
            a * det_2
            - b * c * det_1
        )

        det_1 = det_2
        det_2 = determinant

    return det_2


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
