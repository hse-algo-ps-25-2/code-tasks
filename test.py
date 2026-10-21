import unittest
from itertools import combinations
from random import Random

from dynamic_solver import DynamicSolver
from knapsack_abs_solver import (
    COSTS,
    EMPTY_LIST,
    LENGTHS_NOT_EQUAL,
    LESS_WEIGHT_LIMIT,
    NOT_INT,
    NOT_INT_WEIGHT_LIMIT,
    NOT_LIST,
    NOT_POS,
    NOT_POS_WEIGHT_LIMIT,
    WEIGHTS,
    KnapsackSolution,
)


def check_knapsack_items(weights, costs, weight_limit, result) -> bool:

    items_cnt = len(weights)
    cost = result.cost
    items = result.items
    if len(items) > items_cnt or len(items) == 0:
        return False
    for idx in items:
        if not isinstance(idx, int) or isinstance(idx, bool):
            return False
    if len(set(items)) != len(items):
        return False
    sum_cost = 0
    sum_weight = 0
    for idx in items:
        if idx < 0 or idx >= items_cnt:
            return False
        sum_cost += costs[idx]
        sum_weight += weights[idx]
    if sum_weight > weight_limit:
        return False
    return sum_cost == cost


class TestDynamicSolver(unittest.TestCase):
    def test_2(self):
        """Два предмета"""
        weights = [1, 1]
        costs = [1, 2]
        weight_limit = 1
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 2)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_3(self):
        """Три предмета"""
        weights = [1, 1, 2]
        costs = [1, 2, 2]
        weight_limit = 2
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 3)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_example_from_main(self):
        """Пример из main.py"""
        weights = [11, 4, 8, 6, 3, 5, 5]
        costs = [17, 6, 11, 10, 5, 8, 6]
        weight_limit = 30
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 46)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_not_list_weights(self):
        """Веса не список"""
        with self.assertRaises(TypeError) as error:
            DynamicSolver(1, [1, 1], 1)
        self.assertEqual(NOT_LIST.format(WEIGHTS), str(error.exception))

    def test_not_list_costs(self):
        """Стоимости не список"""
        with self.assertRaises(TypeError) as error:
            DynamicSolver([1], "str", 1)
        self.assertEqual(NOT_LIST.format(COSTS), str(error.exception))


class TestParameterValidation(unittest.TestCase):

    def test_other_not_list_weights(self):
        """None, кортеж, словарь и bool тоже не являются списком весов"""
        for weights in (None, (1, 2), {"weight": 1}, {1, 2}, True, False):
            with self.subTest(weights=weights):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver(weights, [1, 2], 3)
                self.assertEqual(str(error.exception), NOT_LIST.format(WEIGHTS))

    def test_other_not_list_costs(self):
        """Проверка типа нужна для стоимостей независимо от весов"""
        for costs in (None, (1, 2), {"cost": 1}, {1, 2}, True, False):
            with self.subTest(costs=costs):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver([1, 2], costs, 3)
                self.assertEqual(str(error.exception), NOT_LIST.format(COSTS))

    def test_empty_weights(self):
        """Список весов не может быть пустым"""
        with self.assertRaises(ValueError) as error:
            DynamicSolver([], [1], 1)
        self.assertEqual(str(error.exception), EMPTY_LIST.format(WEIGHTS))

    def test_empty_costs(self):
        """Список стоимостей не может быть пустым"""
        with self.assertRaises(ValueError) as error:
            DynamicSolver([1], [], 1)
        self.assertEqual(str(error.exception), EMPTY_LIST.format(COSTS))

    def test_noninteger_weights(self):
        """Проверяются все элементы, включая bool и целочисленный float"""
        for invalid in (None, True, False, 2.0, "2", "abc", [], {}):
            with self.subTest(invalid=invalid):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver([1, invalid], [2, 3], 5)
                self.assertEqual(str(error.exception), NOT_INT.format(WEIGHTS))

    def test_noninteger_costs(self):
        """Неправильный тип стоимости обнаруживается и после верного элемента"""
        for invalid in (None, True, False, 2.0, "2", "abc", [], {}):
            with self.subTest(invalid=invalid):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver([1, 2], [3, invalid], 5)
                self.assertEqual(str(error.exception), NOT_INT.format(COSTS))

    def test_nonpositive_weights(self):
        """Нулевой и отрицательный вес запрещены"""
        for weight in (0, -1, -100):
            with self.subTest(weight=weight):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver([1, weight], [2, 3], 5)
                self.assertEqual(str(error.exception), NOT_POS.format(WEIGHTS))

    def test_nonpositive_costs(self):
        """Нулевая и отрицательная стоимость запрещены"""
        for cost in (0, -1, -100):
            with self.subTest(cost=cost):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver([1, 2], [3, cost], 5)
                self.assertEqual(str(error.exception), NOT_POS.format(COSTS))

    def test_different_lengths(self):
        """длиннее веса и длиннее стоимости"""
        for weights, costs in (([1, 2], [3]), ([1], [2, 3])):
            with self.subTest(weights=weights, costs=costs):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver(weights, costs, 5)
                self.assertEqual(str(error.exception), LENGTHS_NOT_EQUAL)

    def test_noninteger_capacity(self):
        """Вместимость должна быть int; True и False отдельно запрещены"""
        for capacity in (None, True, False, 2.0, "2", [], {}):
            with self.subTest(capacity=capacity):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver([1], [2], capacity)
                self.assertEqual(str(error.exception), NOT_INT_WEIGHT_LIMIT)

    def test_nonpositive_capacity(self):
        """Нулевая и отрицательная вместимость запрещены"""
        for capacity in (0, -1, -100):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver([1], [2], capacity)
                self.assertEqual(str(error.exception), NOT_POS_WEIGHT_LIMIT)

    def test_capacity_below_minimum_weight(self):
        """По этому заданию невозможность взять хоть один предмет — ошибка"""
        with self.assertRaises(ValueError) as error:
            DynamicSolver([3, 5], [4, 6], 2)
        self.assertEqual(str(error.exception), LESS_WEIGHT_LIMIT)


class TestWeightAndCost(unittest.TestCase):

    def test_empty_selection(self):
        """Ничего не выбрать можно; такой набор имеет вес и стоимость ноль"""
        solver = DynamicSolver([2, 3, 4], [3, 4, 5], 5)
        selected = [False, False, False]
        self.assertEqual(solver.get_weight(selected), 0)
        self.assertEqual(solver.get_cost(selected), 0)

    def test_exact_capacity_is_allowed(self):
        """Вес, равный вместимости, не считается перегрузом."""
        solver = DynamicSolver([2, 3, 4], [3, 4, 5], 5)
        self.assertEqual(solver.get_weight([True, True, False]), 5)
        self.assertEqual(solver.get_cost([True, True, False]), 7)

    def test_overweight_cost_is_zero(self):
        """При перегрузе возвращается 0, хотя сумма стоимостей положительна."""
        solver = DynamicSolver([2, 3, 4], [3, 4, 5], 5)
        self.assertEqual(solver.get_cost([True, False, True]), 0)
        self.assertEqual(solver.get_cost([True, True, True]), 0)


class TestDynamicSolverEdgeCases(unittest.TestCase):

    def test_minimum_valid_problem(self):
        """Один предмет и минимальная вместимость 1"""
        result = DynamicSolver([1], [7], 1).get_knapsack()
        self.assertIsInstance(result, KnapsackSolution)
        self.assertEqual(result.cost, 7)
        self.assertTrue(check_knapsack_items([1], [7], 1, result))

    def test_item_cannot_be_used_twice(self):
        """Единственный предмет весом берётся один раз"""
        result = DynamicSolver([2], [3], 6).get_knapsack()
        self.assertEqual(result.cost, 3)
        self.assertTrue(check_knapsack_items([2], [3], 6, result))

    def test_identical_items_have_distinct_indices(self):
        """Два одинаковых предмета можно взять, один предмет дважды — нельзя"""
        weights, costs, capacity = [2, 2, 2], [3, 3, 3], 4
        result = DynamicSolver(weights, costs, capacity).get_knapsack()
        self.assertEqual(result.cost, 6)
        self.assertTrue(check_knapsack_items(weights, costs, capacity, result))

    def test_greedy_cost_per_weight_fails(self):
        """Жадный выбор даёт 160, а правильный набор [1, 2] даёт 220"""
        weights, costs, capacity = [10, 20, 30], [60, 100, 120], 50
        result = DynamicSolver(weights, costs, capacity).get_knapsack()
        self.assertEqual(result.cost, 220)
        self.assertTrue(check_knapsack_items(weights, costs, capacity, result))


class TestKnapsackItemsChecker(unittest.TestCase):

    def test_accepts_any_index_order(self):
        result = KnapsackSolution(cost=7, items=[1, 0])
        self.assertTrue(check_knapsack_items([2, 3, 4], [3, 4, 5], 5, result))

    def test_rejects_invalid_indices(self):
        """Неверные индексы дают False, включая bool и дробные числа."""
        for indices in (
            [],
            [-1],
            [3],
            [0, 0],
            [True],
            [False],
            [1.0],
            ["0"],
            [None],
            [[]],
        ):
            with self.subTest(indices=indices):
                result = KnapsackSolution(cost=3, items=indices)
                self.assertFalse(check_knapsack_items([2, 3, 4], [3, 4, 5], 5, result))


if __name__ == "__main__":
    unittest.main()
