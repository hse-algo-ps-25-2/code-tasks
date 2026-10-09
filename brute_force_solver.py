from knapsack_abs_solver import KnapsackAbstractSolver, KnapsackSolution


class BruteForceSolver(KnapsackAbstractSolver):
    """Решение задачи о рюкзаке полным перебором подмножеств."""

    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает набор максимальной стоимости, не тяжелее вместимости."""
        pass
