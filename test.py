import unittest
from itertools import product
from random import Random

from main import ErrorMessages, ProfitValueError, Result, get_invest_distribution


def _realized_profit(matrix, distribution):
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _assert_optimal_result(test_case, matrix, result, expected_profit):
    levels = len(matrix)
    projects = len(matrix[0])
    test_case.assertIsInstance(result, Result)
    test_case.assertAlmostEqual(result.profit, expected_profit)
    test_case.assertEqual(len(result.distribution), projects)
    test_case.assertEqual(sum(result.distribution), levels)
    for lots in result.distribution:
        test_case.assertIs(type(lots), int)
        test_case.assertGreaterEqual(lots, 0)
        test_case.assertLessEqual(lots, levels)
    test_case.assertAlmostEqual(
        _realized_profit(matrix, result.distribution), expected_profit
    )


class TestInvestDistribution(unittest.TestCase):
    """Набор тестов распределения инвестиций"""

    def test_none(self):
        """Аргумент None"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution(None)
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_bool_value(self):
        """В клетке bool"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[1, True]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_empty(self):
        """Пустой список"""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_negative_profit(self):
        """Отрицательная прибыль"""
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution([[1, -1]])
        self.assertEqual(str(error.exception), ErrorMessages.NEG_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 0)

    def test_decreasing_profit(self):
        """Прибыль убывает по столбцу"""
        matrix = [[1, 1, 1], [2, 3, 2], [2, 2, 3]]
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution(matrix)
        self.assertEqual(str(error.exception), ErrorMessages.DECR_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 2)

    def test_single(self):
        """Один проект и один уровень"""
        matrix = [[1]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 1)

    def test_float_profit(self):
        """Прибыль задана числами float"""
        matrix = [[1.5, 2.0], [3.0, 4.5]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 4.5)

    def test_lecture_table(self):
        """Таблица с лекции: прибыль 73"""
        matrix = [
            [15, 18, 16, 17],
            [20, 22, 23, 19],
            [26, 28, 27, 25],
            [34, 33, 29, 31],
            [40, 39, 41, 37],
        ]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 73)

    def test_invalid_table_types(self):
        for matrix in (42, "table", {}, ((1, 2),), [1, 2], [(1, 2)], [[1], None]):
            with self.subTest(matrix=matrix):
                with self.assertRaises(TypeError) as error:
                    get_invest_distribution(matrix)
                self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_invalid_cell_types(self):
        for value in (None, "2", True, False, 1 + 2j, [], {}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as error:
                    get_invest_distribution([[1, 2], [2, value]])
                self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_invalid_shape(self):
        for matrix in ([[]], [[], []], [[1], []], [[1, 2], [3]], [[1], [2, 3]]):
            with self.subTest(matrix=matrix):
                with self.assertRaises(ValueError) as error:
                    get_invest_distribution(matrix)
                self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_profit_error_coordinates(self):
        cases = (
            ([[-0.5, 1]], ErrorMessages.NEG_PROFIT, 0, 0),
            ([[0, 1], [0, -1]], ErrorMessages.NEG_PROFIT, 1, 1),
            ([[2, 1], [1, 2]], ErrorMessages.DECR_PROFIT, 0, 1),
            ([[1, 1], [2, 2], [3, 1.5]], ErrorMessages.DECR_PROFIT, 1, 2),
        )
        for matrix, message, project_idx, row_idx in cases:
            with self.subTest(matrix=matrix):
                with self.assertRaises(ProfitValueError) as error:
                    get_invest_distribution(matrix)
                self.assertEqual(str(error.exception), message)
                self.assertEqual(error.exception.project_idx, project_idx)
                self.assertEqual(error.exception.row_idx, row_idx)

    def test_one_project(self):
        matrix = [[2], [5], [5], [9]]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 9)

    def test_one_lot(self):
        matrix = [[3, 8, 5, 8]]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 8)

    def test_zero_profit(self):
        matrix = [[0, 0, 0] for _ in range(5)]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 0)

    def test_constant_profit(self):
        matrix = [[4, 3] for _ in range(4)]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 7)

    def test_equal_optimal_plans(self):
        matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 3)

    def test_all_lots_in_one_project(self):
        for best_project in range(3):
            matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
            matrix[-1][best_project] = 20
            with self.subTest(best_project=best_project):
                _assert_optimal_result(
                    self, matrix, get_invest_distribution(matrix), 20
                )

    def test_split_between_projects(self):
        matrix = [[5, 4, 0], [6, 10, 0], [7, 11, 0], [8, 12, 0]]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 16)

    def test_greedy_choice_is_not_optimal(self):
        matrix = [[5, 4], [6, 20]]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 20)

    def test_mixed_numeric_types(self):
        matrix = [[0.1, 0], [0.2, 1], [0.3, 1.05]]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 1.1)

    def test_large_integer_profit(self):
        value = 10**30
        matrix = [[value, value], [value + 1, value + 2]]
        _assert_optimal_result(self, matrix, get_invest_distribution(matrix), 2 * value)

    def test_input_is_not_modified(self):
        matrix = [[1, 2], [3, 5], [6, 7]]
        original = [row[:] for row in matrix]
        first = get_invest_distribution(matrix)
        second = get_invest_distribution(matrix)
        self.assertEqual(matrix, original)
        _assert_optimal_result(self, matrix, first, 7)
        _assert_optimal_result(self, matrix, second, 7)
        self.assertIsNot(first.distribution, second.distribution)

    def test_small_matrices_against_exhaustive_search(self):
        random = Random(42)
        for projects in range(1, 5):
            for lots in range(1, 6):
                for case in range(5):
                    columns = [
                        sorted(random.randint(0, 20) for _ in range(lots))
                        for _ in range(projects)
                    ]
                    matrix = [list(row) for row in zip(*columns)]
                    expected_profit = max(
                        _realized_profit(matrix, distribution)
                        for distribution in product(range(lots + 1), repeat=projects)
                        if sum(distribution) == lots
                    )
                    with self.subTest(projects=projects, lots=lots, case=case):
                        result = get_invest_distribution(matrix)
                        _assert_optimal_result(self, matrix, result, expected_profit)


if __name__ == "__main__":
    unittest.main()
