class Matrix:
    """Класс для операций с матрицами."""

    def __init__(self, matrix: list) -> None:
        self.matrix = matrix

    def is_valid(self) -> bool:
        """Валидация матрицы.

        Проверяет квадратность матрицы
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

        Работает только с квадратными матрицами

        :return: порядок матрицы
        """
        return len(self.matrix)
