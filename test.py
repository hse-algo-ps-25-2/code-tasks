import unittest

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
)


def check_knapsack_items(weights, costs, weight_limit, result) -> bool:
    """Проверяет, что набор укладывается в вместимость и стоимость совпадает"""
    items_cnt = len(weights)
    cost = result.cost
    items = result.items
    if len(items) > items_cnt or len(items) == 0:
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
    """Набор тестов рюкзака динамическим программированием"""

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

    def test_1(self):
        """Один предмет"""
        weights = [3]
        costs = [5]
        weight_limit = 3
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 5)
        self.assertEqual(result.items, [0])

    def test_all_items_fit(self):
        """Помещаются все предметы"""
        weights = [1, 2, 3]
        costs = [4, 5, 6]
        weight_limit = 10
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 15)
        self.assertEqual(sorted(result.items), [0, 1, 2])

    def test_light_items_prefer(self):
        """Два лёгких предмета выгоднее одного тяжёлого"""
        weights = [5, 3, 2]
        costs = [10, 7, 6]
        weight_limit = 5
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 13)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_item_not_duplicate(self):
        """Предмет нельзя взять дважды"""
        weights = [2, 5]
        costs = [10, 1]
        weight_limit = 4
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 10)
        self.assertEqual(result.items, [0])

class TestValidation(unittest.TestCase):
    """Набор тестов для проверки входных данных"""

    def check_error(self, error_type, message, weights, costs, weight_limit):
        with self.assertRaises(error_type) as error:
            DynamicSolver(weights, costs, weight_limit)
        self.assertEqual(message, str(error.exception))

    def test_empty_list(self):
        """Пустой список"""
        self.check_error(ValueError, EMPTY_LIST.format(WEIGHTS), [], [1], 3)
        self.check_error(ValueError, EMPTY_LIST.format(COSTS), [1], [], 3)

    def test_lengths_not_equal(self):
        """Списки разной длины"""
        self.check_error(ValueError, LENGTHS_NOT_EQUAL, [1, 2], [1], 3)
        self.check_error(ValueError, LENGTHS_NOT_EQUAL, [1], [1, 2], 3)

    def test_not_int(self):
        """Нецелое значение в списке"""
        self.check_error(TypeError, NOT_INT.format(WEIGHTS), [1, 2.5], [1, 2], 3)
        self.check_error(TypeError, NOT_INT.format(WEIGHTS), [1, "2"], [1, 2], 3)

    def test_not_positive(self):
        """Нулевое или отрицательное значение в списке"""
        self.check_error(ValueError, NOT_POS.format(WEIGHTS), [0, 1], [1, 2], 3)
        self.check_error(ValueError, NOT_POS.format(WEIGHTS), [1, -2], [1, 2], 3)
        self.check_error(ValueError, NOT_POS.format(COSTS), [1, 2], [0, 1], 3)
        self.check_error(ValueError, NOT_POS.format(COSTS), [1, 2], [1, -5], 3)

    def test_not_int_weight_limit(self):
        """Вместимость не целое число"""
        self.check_error(TypeError, NOT_INT_WEIGHT_LIMIT, [1], [1], 2.5)
        self.check_error(TypeError, NOT_INT_WEIGHT_LIMIT, [1], [1], "3")
        self.check_error(TypeError, NOT_INT_WEIGHT_LIMIT, [1], [1], None)

    def test_not_positive_weight_limit(self):
        """Вместимость меньше единицы"""
        self.check_error(ValueError, NOT_POS_WEIGHT_LIMIT, [1], [1], 0)
        self.check_error(ValueError, NOT_POS_WEIGHT_LIMIT, [1], [1], -3)

    def test_less_weight_limit(self):
        """Вместимость меньше минимального веса"""
        self.check_error(ValueError, LESS_WEIGHT_LIMIT, [5, 7], [1, 2], 4)

    def test_weight_limit_equals_min_weight(self):
        """Вместимость равна минимальному весу - ошибки нет"""
        result = DynamicSolver([5, 7], [1, 2], 5).get_knapsack()
        self.assertEqual(result.cost, 1)
        self.assertEqual(result.items, [0])


if __name__ == "__main__":
    unittest.main()
