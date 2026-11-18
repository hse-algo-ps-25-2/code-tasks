from itertools import pairwise

from error_message_enum import ErrorMessageEnum
from permutation_generator import generate_permutations
from tsp_abs_solver import AbstractTspSolver, NullableNumber, TspSolution


class BruteForceTspSolver(AbstractTspSolver):
    """Полный перебор гамильтоновых циклов"""

    def get_tsp_solution(self) -> TspSolution:
        """Возвращает гамильтонов цикл наименьшей суммарной длины.

        Города — индексы 0, 1, ..., n - 1. Маршрут начинается и заканчивается
        в 0 и содержит каждый город один раз. При n = 1 маршрут — [0],
        расстояние 0. Отсутствующее ребро записано как None. Если цикла нет,
        результат — TspSolution(None, []). Если кратчайших маршрутов несколько,
        годится любой.

        :return: distance — длина маршрута, path — вершины маршрута
        """
        if self.order == 1:
            return TspSolution(0, [0])

        best = TspSolution(None, [])
        matrix = self._dist_matrix
        for permutation in generate_permutations(list(range(1, self.order))):
            path = [0, *permutation, 0]
            if any(matrix[start][end] is None for start, end in pairwise(path)):
                continue

            distance = self.get_distance(matrix, path)
            if best.distance is None or distance < best.distance:
                best = TspSolution(distance, path)

        return best

    def _validate_params(self, matrix: list[list[NullableNumber]]) -> None:
        if isinstance(matrix, list) and any(
            not isinstance(row, list) for row in matrix
        ):
            raise TypeError(ErrorMessageEnum.WRONG_MATRIX)

        try:
            super()._validate_params(matrix)
        except ValueError as error:
            raise ValueError(ErrorMessageEnum.NEG_VALUE) from error
