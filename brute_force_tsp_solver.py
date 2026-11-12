from tsp_abs_solver import AbstractTspSolver, TspSolution


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
        pass
