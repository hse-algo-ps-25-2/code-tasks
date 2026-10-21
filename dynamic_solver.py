from knapsack_abs_solver import KnapsackAbstractSolver, KnapsackSolution


class DynamicSolver(KnapsackAbstractSolver):
    """Решение задачи о рюкзаке динамическим программированием."""

    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает набор максимальной стоимости, не тяжелее вместимости."""
        table = self.fill_table()
        selected_items = self.restore_items(table)
        items = []
        for item_idx in range(self.item_cnt):
            if selected_items[item_idx]:
                items.append(item_idx)
        return KnapsackSolution(cost=self.get_cost(selected_items), items=items)

    def fill_table(self) -> list[list[int]]:
        table = [[0] * (self.weight_limit + 1) for _ in range(self.item_cnt + 1)]

        for item_idx in range(self.item_cnt):
            weight = self.weights[item_idx]
            cost = self.costs[item_idx]

            for weight_idx in range(self.weight_limit):
                current_weight = weight_idx + 1
                table[item_idx + 1][current_weight] = table[item_idx][current_weight]
                if weight <= current_weight:
                    cost_with_item = table[item_idx][current_weight - weight] + cost
                    if cost_with_item > table[item_idx + 1][current_weight]:
                        table[item_idx + 1][current_weight] = cost_with_item

        return table

    def restore_items(self, table: list[list[int]]) -> list[bool]:
        selected_items = [False] * self.item_cnt
        weight = self.weight_limit

        for item_idx in range(self.item_cnt, 0, -1):
            if table[item_idx][weight] != table[item_idx - 1][weight]:
                selected_items[item_idx - 1] = True
                weight -= self.weights[item_idx - 1]
        return selected_items
