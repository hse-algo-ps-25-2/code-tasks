import unittest

from main import (
    INCORRECT_DATA_TYPE,
    TABLE_IS_EMPTY,
    TABLE_NOT_NUMBERS,
    TABLE_NOT_RECT,
    Result,
    get_min_cost_path,
)


def _path_sum(price_table, path):
    return sum(price_table[row][column] for row, column in path)


def _is_allowed_step(previous, current):
    row_delta = current[0] - previous[0]
    column_delta = current[1] - previous[1]
    return (row_delta, column_delta) in {(1, 0), (0, 1)}


def _assert_optimal_result(test_case, price_table, result, expected_cost):
    height = len(price_table)
    width = len(price_table[0])
    test_case.assertEqual(result.cost, expected_cost)
    test_case.assertIsInstance(result.path, list)
    test_case.assertGreaterEqual(len(result.path), 1)
    test_case.assertEqual(result.path[0], (0, 0))
    test_case.assertEqual(result.path[-1], (height - 1, width - 1))
    for previous, current in zip(result.path, result.path[1:]):
        test_case.assertTrue(_is_allowed_step(previous, current))
    test_case.assertEqual(_path_sum(price_table, result.path), expected_cost)


class TestMinCostPath(unittest.TestCase):
    """Набор тестов пути минимальной стоимости"""

    def test_none(self):
        """Аргумент None"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path(None)
        self.assertEqual(str(error.exception), INCORRECT_DATA_TYPE)

    def test_str_value(self):
        """В клетке строка"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, "ab"]])
        self.assertEqual(str(error.exception), TABLE_NOT_NUMBERS)

    def test_bool_value(self):
        """В клетке bool"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, True]])
        self.assertEqual(str(error.exception), TABLE_NOT_NUMBERS)

    def test_empty(self):
        """Пустой список"""
        with self.assertRaises(ValueError) as error:
            get_min_cost_path([])
        self.assertEqual(str(error.exception), TABLE_IS_EMPTY)

    def test_jagged(self):
        """Строки разной длины"""
        with self.assertRaises(ValueError) as error:
            get_min_cost_path([[1.0, 2.0, 3.0], [1.0, 2.0]])
        self.assertEqual(str(error.exception), TABLE_NOT_RECT)

    def test_single(self):
        """Таблица 1 на 1"""
        self.assertEqual(get_min_cost_path([[1]]), Result(cost=1, path=[(0, 0)]))

    def test_double(self):
        """Таблица 2 на 2"""
        table = [[1.1, 2], [3, 4]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=7.1, path=[(0, 0), (0, 1), (1, 1)]),
        )

    def test_triple(self):
        """Таблица 3 на 3"""
        table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(
                cost=8,
                path=[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
            ),
        )

    def test_rectangle(self):
        """Прямоугольная таблица 2 на 3"""
        table = [[1, 2, 2], [3, 4, 1]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=6, path=[(0, 0), (0, 1), (0, 2), (1, 2)]),
        )

    def test_single_float(self):
        """Таблица 1 на 1 с вещественным числом"""
        self.assertEqual(
            get_min_cost_path([[2.5]]),
            Result(cost=2.5, path=[(0, 0)]),
        )

    def test_single_row(self):
        """Таблица 1 на 4"""
        table = [[1, 2, 3, 4]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=10, path=[(0, 0), (0, 1), (0, 2), (0, 3)]),
        )

    def test_single_column(self):
        """Таблица 4 на 1"""
        table = [[1], [2], [3], [4]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=10, path=[(0, 0), (1, 0), (2, 0), (3, 0)]),
        )

    def test_negative_values(self):
        """Отрицательные цены клеток"""
        table = [[-1, -2], [-3, -4]]
        result = get_min_cost_path(table)
        _assert_optimal_result(self, table, result, -8)

    def test_zero_values(self):
        """Нулевые цены клеток"""
        table = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        result = get_min_cost_path(table)
        self.assertEqual(result.cost, 0)
        self.assertEqual(result.path, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)])

    def test_tall_rectangle(self):
        """Прямоугольная таблица 3 на 2"""
        table = [[1, 2], [3, 4], [1, 1]]
        result = get_min_cost_path(table)
        _assert_optimal_result(self, table, result, 6)

    def test_wide_rectangle(self):
        """Прямоугольная таблица 2 на 4"""
        table = [[1, 2, 2, 1], [3, 4, 1, 2]]
        result = get_min_cost_path(table)
        _assert_optimal_result(self, table, result, 8)

    def test_multiple_optimal_paths(self):
        """Несколько путей одинаковой стоимости"""
        table = [[1, 1], [1, 1]]
        result = get_min_cost_path(table)
        _assert_optimal_result(self, table, result, 3)

    def test_large_table(self):
        """Таблица 5 на 5 с единицами"""
        table = [[1] * 5 for _ in range(5)]
        result = get_min_cost_path(table)
        _assert_optimal_result(self, table, result, 9)
        self.assertEqual(len(result.path), 9)

    def test_result_is_namedtuple(self):
        """Результат — именованный кортеж Result"""
        result = get_min_cost_path([[1, 2], [3, 4]])
        self.assertIsInstance(result, Result)
        self.assertEqual(result.cost, result[0])
        self.assertEqual(result.path, result[1])

    def test_path_starts_and_ends(self):
        """Путь начинается в (0, 0) и заканчивается в правом нижнем углу"""
        table = [[2, 1, 5], [1, 2, 3], [4, 1, 1]]
        result = get_min_cost_path(table)
        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (2, 2))
        for previous, current in zip(result.path, result.path[1:]):
            self.assertTrue(_is_allowed_step(previous, current))

    def test_float_table(self):
        """Таблица из вещественных чисел"""
        table = [[0.5, 1.5], [2.5, 0.5]]
        result = get_min_cost_path(table)
        _assert_optimal_result(self, table, result, 2.5)

    def test_mixed_int_float(self):
        """Смешанные int и float клетки"""
        table = [[1, 2.5], [3.5, 4]]
        result = get_min_cost_path(table)
        _assert_optimal_result(self, table, result, 7.5)

    def test_none_inside_row(self):
        """В клетке None"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, None]])
        self.assertEqual(str(error.exception), TABLE_NOT_NUMBERS)

    def test_list_inside_row(self):
        """В клетке список"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, [2]]])
        self.assertEqual(str(error.exception), TABLE_NOT_NUMBERS)

    def test_row_not_list(self):
        """Строка таблицы — не список"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path((1, 2))
        self.assertEqual(str(error.exception), INCORRECT_DATA_TYPE)

    def test_empty_rows(self):
        """Строка нулевой длины"""
        with self.assertRaises(ValueError) as error:
            get_min_cost_path([[], []])
        self.assertEqual(str(error.exception), TABLE_IS_EMPTY)

    def test_one_empty_row(self):
        """Таблица из одной пустой строки"""
        with self.assertRaises(ValueError) as error:
            get_min_cost_path([[]])
        self.assertEqual(str(error.exception), TABLE_IS_EMPTY)


if __name__ == "__main__":
    unittest.main()
