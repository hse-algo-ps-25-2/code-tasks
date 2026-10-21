import itertools
import random
import unittest

from main import ErrorMessages, ProfitValueError, get_invest_distribution


def _realized_profit(matrix, distribution):
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _brute_force_profit(matrix):
    """Максимальная прибыль полным перебором всех распределений"""
    levels = len(matrix)
    projects = len(matrix[0])
    best = 0
    for allocation in itertools.product(range(levels + 1), repeat=projects):
        if sum(allocation) != levels:
            continue
        best = max(best, _realized_profit(matrix, list(allocation)))
    return best


def _assert_optimal_result(test_case, matrix, result, expected_profit):
    levels = len(matrix)
    projects = len(matrix[0])
    test_case.assertEqual(result.profit, expected_profit)
    test_case.assertEqual(len(result.distribution), projects)
    test_case.assertEqual(sum(result.distribution), levels)
    for lots in result.distribution:
        test_case.assertGreaterEqual(lots, 0)
        test_case.assertLessEqual(lots, levels)
    test_case.assertEqual(
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

    def test_argument_not_a_list(self):
        """Аргумент не список"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution("table")
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_row_not_a_list(self):
        """Строка таблицы не список"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([(1, 2)])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_cell_not_a_number(self):
        """В клетке строка"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[1, "2"]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_not_rectangular(self):
        """Строки разной длины"""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([[1, 2], [3]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_empty_row(self):
        """Таблица с пустой строкой"""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([[], [1]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_decreasing_profit_second_row(self):
        """Прибыль убывает на второй строке"""
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution([[5], [4]])
        self.assertEqual(str(error.exception), ErrorMessages.DECR_PROFIT)
        self.assertEqual(error.exception.project_idx, 0)
        self.assertEqual(error.exception.row_idx, 1)

    def test_equal_profit_allowed(self):
        """Ненулевой прирост не обязателен: равные значения допустимы"""
        matrix = [[5, 5], [5, 5]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 10)

    def test_all_lots_to_one_project(self):
        """Оптимум — все лоты в один проект"""
        matrix = [[10, 1], [20, 2], [30, 3]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 30)

    def test_split_between_projects(self):
        """Разделение лотов между проектами выгоднее концентрации"""
        matrix = [[5, 5], [8, 8], [10, 10]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 13)

    def test_symmetric_table(self):
        """Любое распределение оптимально"""
        matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 3)

    def test_single_project_many_lots(self):
        """Один проект и несколько лотов"""
        matrix = [[1], [2], [3], [4]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 4)

    def test_matches_brute_force(self):
        """Динамическое программирование совпадает с полным перебором"""
        random.seed(42)
        for _ in range(20):
            levels = random.randint(1, 5)
            projects = random.randint(1, 4)
            columns = []
            for _ in range(projects):
                value = 0
                column = []
                for _ in range(levels):
                    value += random.randint(0, 5)
                    column.append(value)
                columns.append(column)
            matrix = [list(row) for row in zip(*columns)]
            result = get_invest_distribution(matrix)
            self.assertEqual(result.profit, _brute_force_profit(matrix))
            self.assertEqual(sum(result.distribution), levels)
            self.assertEqual(len(result.distribution), projects)
            self.assertEqual(
                _realized_profit(matrix, result.distribution), result.profit
            )


if __name__ == "__main__":
    unittest.main()
