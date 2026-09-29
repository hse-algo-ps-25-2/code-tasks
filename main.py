def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной матрицы разложением.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    if matrix is None:
        raise Exception("matrix must be not None")

    if matrix == []:
        raise Exception("matrix must be not empty")
    
    n = len(matrix)

    # Базовый случай, исключений быть не может
    if n == 1 and len(matrix[0]) == 0:
        return 1
    
    # При рекурсивном обходе матрицы мы удостоверяемся ,что она квадратная
    if n != len(matrix[0]):
        raise Exception("matrix should be square")

    a = matrix[0][0]
    # Если базовый случай так же квадратный, то всё ок и мы возвращаем базу
    if n == 1:
        return a

    b, c = matrix[0][1], matrix[1][0]
    # По двум направлениям проверяем, что марица трехдиагональная 
    for el in matrix[0][2:]:
        if el != 0:
            raise Exception("matrix must be tridiagonal")

    for i in range(2, n):
        if matrix[i][0] != 0:
            raise Exception("matrix must be tridiagonal")

    minor_1 = [row[1:] for row in matrix[1:]]
    minor_2 = [row[2:] for row in matrix[2:]]
    # По алгебраическим дополнениям раскладываем определитель
    return a * get_tridiagonal_determinant(minor_1 if minor_1 else [[]]) - \
           b * c * get_tridiagonal_determinant(minor_2 if minor_2 else [[]])


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
