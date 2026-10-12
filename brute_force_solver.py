from knapsack_abs_solver import KnapsackAbstractSolver, KnapsackSolution


class BruteForceSolver(KnapsackAbstractSolver):
    """Решение задачи о рюкзаке полным перебором подмножеств."""

    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает набор максимальной стоимости, не тяжелее вместимости."""
        weights = self.weights
        costs = self.costs
        weight_limit =self.weight_limit

        n = len(costs)
        sets = [[]]

        for i in range(n):
            new_sets = []
            for set in sets:
                new_sets.append(set)
                new_sets.append(set + [i])
            sets = new_sets

        best_cost = 0
        best_set = []

        for set in sets:
            weight = 0
            cost = 0

            for i in set:
                weight += weights[i]
                cost += costs[i]

            if cost > best_cost and not weight > weight_limit:
                best_cost = cost
                best_set = set
        
        return KnapsackSolution(best_cost, best_set)
