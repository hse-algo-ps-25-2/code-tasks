from knapsack_abs_solver import KnapsackAbstractSolver, KnapsackSolution


class DynamicSolver(KnapsackAbstractSolver):
    """Решение задачи о рюкзаке динамическим программированием."""

    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает набор максимальной стоимости, не тяжелее вместимости."""
        table = self.fill_table()
        selected_items = self.restore_items(table)
        items = []
        for cost_idx in range(self.item_cnt):
            if selected_items[cost_idx]:
                items.append(cost_idx)
        return KnapsackSolution(cost=self.get_cost(selected_items), items=items)

    def fill_table(self) -> list[list[int]]:
        table = [[0] * (self.weight_limit + 1) for _ in range(self.item_cnt + 1)]

        for cost_idx in range(self.item_cnt):
            weight = self.weights[cost_idx]
            cost = self.costs[cost_idx]

            for weight_idx in range(self.weight_limit):
                table[cost_idx + 1][weight_idx + 1] = table[cost_idx][weight_idx + 1]
                if (weight <= weight_idx
                        and table[cost_idx][weight_idx - weight + 1] + cost > table[cost_idx + 1][weight_idx + 1]):
                    table[cost_idx + 1][weight_idx + 1] = table[cost_idx][weight_idx - weight + 1] + cost

        return table

    def restore_items(self, table: list[list[int]]) -> list[bool]:
        selected_items = [False] * self.item_cnt
        weight = self.weight_limit

        for cost_idx in range(self.item_cnt, 0, -1):
            if table[cost_idx][weight] != table[cost_idx - 1][weight]:
                selected_items[cost_idx - 1] = True
                weight -= self.weights[cost_idx - 1]
        return selected_items
