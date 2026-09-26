import unittest

from main import calculate_determinant
from matrix_generator import generate_matrix_and_det


def require_generator(test_case):
    sample = generate_matrix_and_det(1)
    if sample is None:
        test_case.skipTest("Generator is not implemented")
    return sample


class TestDeterminant(unittest.TestCase):
    """Набор тестов для проверки функции вычисления определителя
    целочисленной квадратной матрицы"""

    def test_none(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения None"""
        self.assertRaises(Exception, calculate_determinant, None)

    def test_empty_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого списка"""
        self.assertRaises(Exception, calculate_determinant, [])

    def test_not_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы"""
        matrix = [[3, -3, -5, 8], [-3, 2, 4, -6], [-4, 3, 5, -6]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_not_even_square(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы, у которой количество в строке не хватает значений
        """
        matrix = [[1, 2], [3]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_invalid_float_cell_value(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы, у которой в ячейке дробное значение
        """
        matrix = [[1, 2], [3, 4.5]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_invalid_bool_cell_value(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы, у которой в ячейке булево значение
        """
        matrix = [[1, 2], [3, True]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_none_cell_value(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы, у которой в ячейке пустое значение
        """
        matrix = [[1, 2], [3, None]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_first_order(self):
        """Проверяет расчет определителя для матрицы порядка 1"""
        matrix = [[1]]
        self.assertEqual(calculate_determinant(matrix), 1)

    def test_second_order(self):
        """Проверяет расчет определителя для матрицы порядка 2"""
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(calculate_determinant(matrix), -2)

    def test_third_order(self):
        """Проверяет расчет определителя для матрицы порядка 3"""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]
        self.assertEqual(calculate_determinant(matrix), -3)

    def test_fourth_order(self):
        """Проверяет расчет определителя для матрицы порядка 4"""
        matrix = [[3, -3, -5, 8], [-3, 2, 4, -6], [2, -5, -7, 5], [-4, 3, 5, -6]]
        self.assertEqual(calculate_determinant(matrix), 18)

    def test_zero_row_matrix(self):
        """Проверяет, что функция возвращает 0 для матрицы c нулевой строкой"""
        matrix = [[0, 0, 0], [1, 2, 3], [4, 5, 6]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_zero_column_matrix(self):
        """Проверяет, что функция возвращает 0 для матрицы c нулевым столбцом"""
        matrix = [[0, 1, 2], [0, 3, 4], [0, 5, 6]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_linearly_dependent_matrix(self):
        """Проверяет, что функция возвращает 0 для матрицы
        с линейно зависимыми строками"""
        matrix = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_large_numbers(self):
        """Проверяет, что функция возвращает большие числа"""
        matrix = [[10**10, 0], [0, 10**10]]
        self.assertEqual(calculate_determinant(matrix), 10**20)

    def test_large_numbers_with_reduction(self):
        """Проверяет, что функция корректно обрабатывает большие числа
        при условии когда результат сокращается до малого значения"""
        matrix = [[10**10, 10**10 - 1], [10**10 + 1, 10**10]]
        self.assertEqual(calculate_determinant(matrix), 1)

    def test_generator(self):
        """Проверяет генератор матриц с известным определителем"""
        require_generator(self)
        for order in range(1, 11):
            with self.subTest(order=order):
                test_case = generate_matrix_and_det(order)
                self.assertEqual(len(test_case.matrix), order)
                for row in test_case.matrix:
                    self.assertEqual(len(row), order)
                self.assertEqual(calculate_determinant(test_case.matrix), test_case.det)


if __name__ == "__main__":
    unittest.main()
