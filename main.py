from matrix import Matrix


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель разложением по строке.

    :param matrix: квадратная целочисленная матрица порядка не меньше 1
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    m = Matrix(matrix)

    if not m.is_valid():
        raise Exception("Введённая матрица не является квадратной")

    n = m.get_size()

    if n == 1:
        return m.get_element(0, 0)

    det = 0

    for j in range(n):
        element = m.get_element(0, j)
        sign = (-1) ** j
        minor = m.get_minor(0, j)
        det += element * sign * calculate_determinant(minor)

    return det


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
