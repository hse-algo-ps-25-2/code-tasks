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


    for i in range(n):
        for j in range(n):
            if i == j:
                if matrix[i][j] != a:
                    raise Exception("Значения на главной диагонали не постоянны")
            elif i == j - 1:
                if matrix[i][j] != b:
                    raise Exception("Значения на наддиагонали не постоянны")
            elif i == j + 1:
                if matrix[i][j] != c:
                    raise Exception("Значения на поддиагонали не постоянны")
            else:
                if matrix[i][j] != 0:
                    raise Exception("Внедиагональные элементы должны быть равны нулю")

memo = {}

    def recursive_det(k: int) -> int:
        if k == 1:
            return a
        if k == 2:
            return a * a - b * c
        if k in memo:
            return memo[k]
        
        # Формула разложения по строке: D_k = a * D_{k-1} - b * c * D_{k-2}
        res = a * recursive_det(k - 1) - b * c * recursive_det(k - 2)
        memo[k] = res
        return res

    return recursive_det(n)



def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
