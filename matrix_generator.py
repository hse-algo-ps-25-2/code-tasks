import random
from collections import namedtuple

Case = namedtuple("Case", ["matrix", "det"])


def swap_rows(order, matrix, det):
    """Переставляет случайные пары строк. По свойству матриц,
    каждая перестановка меняет знак определителя.

    :param order: порядок матрицы, целое число не меньше 1
    :param matrix: матрица
    :param det: определитель матрицы
    :return: det
    """
    for i in range(order - 1):
        j = random.randint(i + 1, order - 1)
        matrix[i], matrix[j] = matrix[j], matrix[i]
        det = det * (-1)
    return det


def sum_rows(order, matrix):
    """Прибавляет к первой строке остальные строки, умноженные на константу.
    Затем прибавляет первую строку, умноженную на константу, к остальным строкам.
    Прибавление строки, умноженной на константу, не меняет определитель.

    :param order: порядок матрицы, целое число не меньше 1
    :param matrix: матрица
    """
    for i in range(1, order):
        k = random.randint(1, 10) * random.choice((-1, 1))
        for j in range(order):
            matrix[0][j] += matrix[i][j] * k

    for i in range(1, order):
        k = random.randint(1, 10) * random.choice((-1, 1))
        for j in range(order):
            matrix[i][j] += matrix[0][j] * k


def generate_matrix_and_det(order: int) -> Case:
    """Строит квадратную целочисленную матрицу заданного порядка
    с заранее известным определителем.

    Определитель получают из свойств, не вычисляя его разложением
    и не вызывая calculate_determinant.

    :param order: порядок матрицы, целое число не меньше 1
    :raises Exception: если order не является таким числом
    :return: Case с полями matrix и det
    """
    if not isinstance(order, int) or order < 1:
        raise Exception("order должен быть целым числом >= 1")

    det = 1
    matrix = []

    for i in range(order):
        row = [0] * order
        matrix.append(row)
        matrix[i][i] = random.randint(1, 10)
        det = det * matrix[i][i]

    det = swap_rows(order, matrix, det)
    sum_rows(order, matrix)

    return Case(matrix=matrix, det=det)


def main():
    n = 10
    print(f"Генерация матрицы порядка {n}")
    result = generate_matrix_and_det(n)
    print("\nОпределитель сгенерированной матрицы равен", result.det)
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in result.matrix]))


if __name__ == "__main__":
    main()
