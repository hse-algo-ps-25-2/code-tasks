from abc import ABC, abstractmethod
from collections import namedtuple

from error_message_enum import ErrorMessageEnum

TspSolution = namedtuple("TspSolution", ["distance", "path"])
NullableNumber = int | float | None


class AbstractTspSolver(ABC):
    """Абстрактный класс для решения задачи коммивояжера"""

    def __init__(self, dist_matrix: list[list[NullableNumber]]) -> None:
        """Создаёт объект для решения задачи коммивояжера.

        :param dist_matrix: матрица расстояний
        :raises TypeError: Таблица расстояний не является прямоугольной
            матрицей с числовыми значениями
        :raises ValueError: Расстояние не может быть отрицательным
        """
        self._validate_params(dist_matrix)
        self._dist_matrix = dist_matrix

    @property
    def order(self):
        """Возвращает порядок матрицы расстояний"""
        return len(self._dist_matrix)

    @abstractmethod
    def get_tsp_solution(self) -> TspSolution:
        """Возвращает кратчайший гамильтонов цикл.

        :return: distance — длина маршрута, path — вершины маршрута
        """
        pass

    def get_distance(
        self, dist_matrix: list[list[NullableNumber]], path: list[int]
    ) -> float:
        """Возвращает суммарную длину маршрута по последовательным рёбрам.

        :param dist_matrix: матрица расстояний
        :param path: вершины маршрута
        """
        pass

    def _validate_params(self, matrix: list[list[NullableNumber]]) -> None:
        """Проверяет, что матрица прямоугольная и длины рёбер неотрицательны."""
        if (
            not matrix
            or not isinstance(matrix, list)
            or not matrix[0]
            or not isinstance(matrix[0], list)
        ):
            raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
        row_len = len(matrix[0])
        if row_len != len(matrix):
            raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
        for row_idx in range(len(matrix)):
            if len(matrix[row_idx]) != row_len:
                raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
            for col_idx in range(row_len):
                if not isinstance(matrix[row_idx][col_idx], NullableNumber):
                    raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
                if matrix[row_idx][col_idx] and matrix[row_idx][col_idx] < 0:
                    raise ValueError(ErrorMessageEnum.NEG_VALUE, col_idx, row_idx)
