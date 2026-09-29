def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Итеративное вычисление определителя трёхдиагональной матрицы.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    if matrix is None:
        raise Exception("matrix is None")

    if not isinstance(matrix, list):
        raise Exception("matrix is not list")
    
    if not matrix:
        raise Exception("matrix is empty")


    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise Exception("matrix is not square")
    
    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and matrix[i][j] != 0:
                raise Exception("matrix is not tridiagonal")
        
    a = matrix[0][0]
    b = matrix[0][1] if n > 1 else 0
    c = matrix[1][0] if n > 1 else 0

    for i in range(n):
        if matrix[i][i] != a:
            raise Exception('main diagonal is not constant') 
        if i + 1 < n and matrix[i][i+1] != b:
            raise Exception('upper diagonal is not constant')
        if i + 1 < n and matrix[i+1][i] != c:
            raise Exception('lower diagonal is not constant') 
    
    if n == 1:
        return a

    prev2 = 1
    prev1 = a

    for _ in range(2, n + 1):
        current = a * prev1 - b * c * prev2
        prev2 = prev1
        prev1 = current

    return prev1


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
