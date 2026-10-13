import unittest

from brute_force_solver import BruteForceSolver
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
)


def check_knapsack_items(weights, costs, weight_limit, result) -> bool:
    """Проверяет, что набор укладывается в вместимость и стоимость совпадает"""
    items_cnt = len(weights)
    cost = result.cost
    items = result.items
    if len(items) > items_cnt or len(items) == 0:
        return False
    sum_cost = 0
    sum_weight = 0
    for idx in items:
        if idx >= items_cnt:
            return False
        sum_cost += costs[idx]
        sum_weight += weights[idx]
    if sum_weight > weight_limit:
        return False
    return sum_cost == cost


class TestBruteForceSolver(unittest.TestCase):
    """Тесты решения задачи о рюкзаке"""

    def test_one_item(self):
        """Один предмет"""
        weights = [5]
        costs = [7]
        weight_limit = 5
        result = BruteForceSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 7)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_two_items(self):
        """Два предмета"""
        weights = [1, 1]
        costs = [1, 2]
        weight_limit = 1
        result = BruteForceSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 2)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_three_items(self):
        """Три предмета"""
        weights = [1, 1, 2]
        costs = [1, 2, 2]
        weight_limit = 2
        result = BruteForceSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 3)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_all_items_fit(self):
        """Помещаются все предметы"""
        weights = [2, 3, 4]
        costs = [5, 6, 7]
        weight_limit = 100
        result = BruteForceSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 18)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_exact_limit(self):
        """Вес набора ровно равен вместимости"""
        weights = [3, 4, 5]
        costs = [4, 5, 6]
        weight_limit = 9
        result = BruteForceSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 11)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_most_expensive_not_in_answer(self):
        """Самый дорогой предмет не входит в лучший набор"""
        weights = [10, 4, 4, 2]
        costs = [10, 5, 5, 3]
        weight_limit = 10
        result = BruteForceSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 13)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_main_example(self):
        """Пример из main.py"""
        weights = [11, 4, 8, 6, 3, 5, 5]
        costs = [17, 6, 11, 10, 5, 8, 6]
        weight_limit = 30
        result = BruteForceSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 46)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))


class TestWeightAndCost(unittest.TestCase):
    """Тесты get_weight и get_cost"""

    def test_get_weight(self):
        """Вес выбранных предметов"""
        solver = BruteForceSolver([2, 3, 5], [10, 20, 30], 10)
        self.assertEqual(solver.get_weight([True, False, True]), 7)

    def test_get_weight_empty(self):
        """Вес пустого набора"""
        solver = BruteForceSolver([2, 3, 5], [10, 20, 30], 10)
        self.assertEqual(solver.get_weight([False, False, False]), 0)

    def test_get_cost(self):
        """Стоимость выбранных предметов"""
        solver = BruteForceSolver([2, 3, 5], [10, 20, 30], 10)
        self.assertEqual(solver.get_cost([False, True, True]), 50)

    def test_get_cost_overweight(self):
        """Стоимость набора тяжелее вместимости равна 0"""
        solver = BruteForceSolver([2, 3, 5], [10, 20, 30], 7)
        self.assertEqual(solver.get_cost([True, True, True]), 0)

    def test_weight_limit_equal_min_possible_weight(self):
        """Вместимость равна минимальному весу"""
        solver = BruteForceSolver([5, 7], [1, 1], 5)
        self.assertEqual(solver.get_cost([True, False]), 1)


class TestValidation(unittest.TestCase):
    """Проверка входных данных"""

    def test_not_list_weights(self):
        """Веса не список"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver(1, [1, 1], 1)
        self.assertEqual(NOT_LIST.format(WEIGHTS), str(error.exception))

    def test_not_list_costs(self):
        """Стоимости не список"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([1], "str", 1)
        self.assertEqual(NOT_LIST.format(COSTS), str(error.exception))

    def test_empty_weights(self):
        """Веса — пустой список"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([], [1], 1)
        self.assertEqual(EMPTY_LIST.format(WEIGHTS), str(error.exception))

    def test_empty_costs(self):
        """Стоимости — пустой список"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([1], [], 1)
        self.assertEqual(EMPTY_LIST.format(COSTS), str(error.exception))

    def test_not_int_weights(self):
        """Веса содержат дробное число"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([1, 2.5], [1, 1], 3)
        self.assertEqual(NOT_INT.format(WEIGHTS), str(error.exception))

    def test_not_int_costs(self):
        """Стоимости содержат дробное число"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([1, 2], [1.5, 1], 3)
        self.assertEqual(NOT_INT.format(COSTS), str(error.exception))

    def test_not_pos_weights(self):
        """Веса содержат ноль"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([1, 0], [1, 1], 3)
        self.assertEqual(NOT_POS.format(WEIGHTS), str(error.exception))

    def test_not_pos_costs(self):
        """Стоимости содержат отрицательное значение"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([1, 2], [1, -5], 3)
        self.assertEqual(NOT_POS.format(COSTS), str(error.exception))
    
    def test_str_weights(self):
        """Стоимости содержат строковое значение"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([1, "2"], [1, 5], 3)
        self.assertEqual(NOT_INT.format(WEIGHTS), str(error.exception))

    def test_str_costs(self):
        """Стоимости содержат строковое значение"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([1, 2], [1, "5"], 3)
        self.assertEqual(NOT_INT.format(COSTS), str(error.exception))

    def test_lengths_not_equal(self):
        """Списки разной длины"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([1, 2], [1, 2, 3], 3)
        self.assertEqual(LENGTHS_NOT_EQUAL, str(error.exception))

    def test_not_int_weight_limit(self):
        """Вместимость не целое число"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([1], [1], 1.5)
        self.assertEqual(NOT_INT_WEIGHT_LIMIT, str(error.exception))

    def test_negative_weight_limit(self):
        """Вместимость равна нулю"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([1], [1], -2)
        self.assertEqual(NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_not_pos_weight_limit(self):
        """Вместимость равна нулю"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([1], [1], 0)
        self.assertEqual(NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_less_weight_limit(self):
        """Вместимость меньше минимального веса"""
        with self.assertRaises(ValueError) as error:
            BruteForceSolver([5, 7], [1, 1], 4)
        self.assertEqual(LESS_WEIGHT_LIMIT, str(error.exception))

    def test_weights_limits_boolean_param(self):
        """Ошибка при boolean в лимите веса"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([2, 7], [1, 2], True)
        self.assertEqual(NOT_INT_WEIGHT_LIMIT, str(error.exception))

    def test_weights_boolean_param(self):
        """Ошибка при boolean в весах"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([True, 7], [1, 2], 4)
        self.assertEqual(NOT_INT.format(WEIGHTS), str(error.exception))
    
    def test_costs_boolean_param(self):
        """Ошибка при boolean в стоимостях"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([5, 7], [True, True], 4)
        self.assertEqual(NOT_INT.format(COSTS), str(error.exception))

    def test_weights_tuple_param(self):
        """Ошибка при boolean в стоимостях"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver((1, 2), [5, 7], 4)
        self.assertEqual(NOT_LIST.format(WEIGHTS), str(error.exception))
    
    def test_costs_tuple_param(self):
        """Ошибка при boolean в стоимостях"""
        with self.assertRaises(TypeError) as error:
            BruteForceSolver([5, 7], (1, 2), 4)
        self.assertEqual(NOT_LIST.format(COSTS), str(error.exception))

if __name__ == "__main__":
    unittest.main()