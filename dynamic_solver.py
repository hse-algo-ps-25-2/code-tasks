from knapsack_abs_solver import KnapsackAbstractSolver, KnapsackSolution


class DynamicSolver(KnapsackAbstractSolver):

    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает набор максимальной стоимости, не тяжелее вместимости"""
        # dp[i][capacity]: лучшая стоимость среди первых i предметов.
        dp = [[0] * (self.weight_limit + 1) for _ in range(self.item_cnt + 1)]

        for i in range(1, self.item_cnt + 1):
            weight = self.weights[i - 1]
            cost = self.costs[i - 1]

            for capacity in range(1, self.weight_limit + 1):
                without_item = dp[i - 1][capacity]
                dp[i][capacity] = without_item

                if weight <= capacity:
                    with_item = dp[i - 1][capacity - weight] + cost
                    dp[i][capacity] = max(without_item, with_item)

        # Восстанавливаем набор; при равенстве пропускаем текущий предмет.
        selected_items = [False] * self.item_cnt
        capacity = self.weight_limit
        for i in range(self.item_cnt, 0, -1):
            if dp[i][capacity] != dp[i - 1][capacity]:
                selected_items[i - 1] = True
                capacity -= self.weights[i - 1]

        items = []
        for index in range(self.item_cnt):
            if selected_items[index]:
                items.append(index)

        # Родительский get_cost проверяет вес через get_weight.
        return KnapsackSolution(cost=self.get_cost(selected_items), items=items)
