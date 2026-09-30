def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:

    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise Exception("Матрица должна быть списком списков")

    n = len(matrix)
    if n < 1:
        raise Exception("Порядок матрицы должен быть не меньше 1")

    for row in matrix:
        if len(row) != n:
            raise Exception("Матрица должна быть квадратной")
        if not all(isinstance(elem, int) for elem in row):
            raise Exception("Элементы матрицы должны быть целыми числами")

    a = matrix[0][0]  # Главная диагональ
    b = matrix[0][1] if n > 1 else 0  # Наддиагональ
    c = matrix[1][0] if n > 1 else 0  # Поддиагональ

    diagonals = {0: a, 1: b, -1: c}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != diagonals.get(j - i, 0):
                raise Exception("Матрица должна иметь три постоянные диагонали")

    return _recursive_det(n, a, b, c, {})


def _recursive_det(k: int, a: int, b: int, c: int, memo: dict[int, int]) -> int:
    if k == 1:
        return a
    if k == 2:
        return a * a - b * c
    if k in memo:
        return memo[k]

    # Формула разложения по строке: D_k = a * D_{k-1} - b * c * D_{k-2}.
    res = a * _recursive_det(k - 1, a, b, c, memo) - b * c * _recursive_det(
        k - 2, a, b, c, memo
    )
    memo[k] = res
    return res


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
