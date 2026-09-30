class Matrix:
    """Класс для операций с матрицами."""

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    def is_valid(self) -> bool:
        """Валидация матрицы.

        Проверяет, что матрица квадратная и непустая
        """

        height = len(self.matrix)

        if height <= 0:
            return False

        for i in self.matrix:
            if len(i) != height:
                return False
        return True

    def get_size(self) -> int:
        """Вычисление порядка матрицы.

        Работает корректно исключительно с квадратными матрицами

        :return: порядок матрицы
        """
        return len(self.matrix)

    def get_element(self, row: int, column: int) -> int:
        """Возвращает элемент матрицы по его строке и столбцу."""
        return self.matrix[row][column]

    def get_minor(self, row: int, column: int) -> list[list[int]]:
        """Возвращает исходную матрицу без i-ой строки и j-ого столбца."""
        matrix = self.matrix

        if not (0 <= row < len(matrix)):
            raise IndexError(f"Строк в матрице {len(matrix)}, а запрашивается {row}")

        elif not (0 <= column < len(matrix[0])):
            raise IndexError(
                f"Столбцов в матрице {len(matrix[0])}, а запрашивается {column}"
            )

        matrix_without_row = matrix[:row] + matrix[row + 1 :]

        new_matrix = []

        for matrix_row in matrix_without_row:
            new_matrix.append(matrix_row[:column] + matrix_row[column + 1 :])

        return new_matrix
