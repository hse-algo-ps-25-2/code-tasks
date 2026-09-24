from collections import namedtuple

Case = namedtuple("Case", ["matrix", "det"])


def generate_matrix_and_det(order: int) -> Case:
    """Строит квадратную целочисленную матрицу заданного порядка
    с заранее известным определителем.

    Определитель получают из свойств, не вычисляя его разложением
    и не вызывая calculate_determinant.

    :param order: порядок матрицы, целое число не меньше 1
    :raises Exception: если order не является таким числом
    :return: Case с полями matrix и det
    """
    pass


def main():
    n = 10
    print(f"Генерация матрицы порядка {n}")
    result = generate_matrix_and_det(n)
    print("\nОпределитель сгенерированной матрицы равен", result.det)
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in result.matrix]))


if __name__ == "__main__":
    main()
