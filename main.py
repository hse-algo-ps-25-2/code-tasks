def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной матрицы разложением.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    validate (matrix)

    n = len(matrix)

    a = matrix [0][0]
    b = matrix [0][1] if n > 1 else 0
    c = matrix [1][0] if n > 1 else 0

    return determinant(a, b, c, n)

def determinant(a, b, c, n):
    if n == 1:
        return a 
    if n == 2:
        return a * a - b * c
    
    return a * determinant(a, b, c, n - 1) - b * c * determinant(a, b, c, n - 2)


def validate(matrix):
    n = len(matrix)

    if not isinstance(matrix, list) or n == 0:
        raise Exception ("Данная матрица - пустой список!")

    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise Exception ("Данная матрица не квадратная!")


    a = matrix [0][0]
    if n > 1:
        b = matrix [0][1]
        c = matrix [1][0]

    for i in range(n):
        for j in range(n):
            value = matrix[i][j]
            if type(value) is not int:
                raise Exception ("В данной матрице есть нецелые элементы!")
            
            if abs(i - j) > 1 and value != 0:
                raise Exception ("В данной матрице есть ненулевые элементы вне трёх диагоналей!")

            if i == j and value != a:
                raise Exception ("В данной матрице элементы главной диагонали не постоянны!")

            if n > 1 and (i + 1) == j and value != b:
                raise Exception ('В данной матрице элементы "верхней" диагонали не постоянны!')

            if n > 1 and i == (j + 1) and value != c:
                raise Exception ('В данной матрице элементы "нижней" диагонали не постоянны!')

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
