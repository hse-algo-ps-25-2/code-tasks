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
        matrix = [[1, -2, 3], [-4, 5, -6], [7, -8, 9]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_fourth_order(self):
        """Проверяет расчет определителя для матрицы порядка 4"""
        matrix = [[3, -3, -5, 8], [-3, 2, 4, -6], [2, -5, -7, 5], [-4, 3, 5, -6]]
        self.assertEqual(calculate_determinant(matrix), 18)

    def test_invalid_matrix_type(self):
        for matrix in (1, 1.0, True, "1", {0: [1]}):
            with self.subTest(matrix=matrix):
                self.assertRaises(Exception, calculate_determinant, matrix)

    def test_invalid_row_type(self):
        for matrix in ([1], [None], ["1"], [[1, 2], None]):
            with self.subTest(matrix=matrix):
                self.assertRaises(Exception, calculate_determinant, matrix)

    def test_invalid_row_length(self):
        for matrix in ([[]], [[1, 2], [3]], [[1], [2]], [[1, 2], [3, 4, 5]]):
            with self.subTest(matrix=matrix):
                self.assertRaises(Exception, calculate_determinant, matrix)

    def test_non_integer_elements(self):
        for value in (1.0, "1", None, True, False, 1 + 0j, [], {}):
            with self.subTest(value=value):
                self.assertRaises(Exception, calculate_determinant, [[value]])
                self.assertRaises(
                    Exception, calculate_determinant, [[0, 0], [0, value]]
                )

    def test_first_order_zero_and_negative(self):
        for value in (0, -7):
            with self.subTest(value=value):
                self.assertEqual(calculate_determinant([[value]]), value)

    def test_triangular_matrix(self):
        matrix = [[-2, 0, 0, 0], [3, 5, 0, 0], [1, -4, -3, 0], [2, 8, 6, 7]]
        self.assertEqual(calculate_determinant(matrix), 210)

    def test_identity_matrix(self):
        order = 5
        matrix = [
            [int(row == column) for column in range(order)] for row in range(order)
        ]
        self.assertEqual(calculate_determinant(matrix), 1)

    def test_zero_row(self):
        matrix = [[1, 2, 3], [0, 0, 0], [4, 5, 6]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_equal_rows(self):
        matrix = [[2, -3, 4], [5, 6, 7], [2, -3, 4]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_row_swap_changes_sign(self):
        matrix = [[0, 2, 0], [3, 0, 0], [0, 0, 4]]
        self.assertEqual(calculate_determinant(matrix), -24)
        matrix[0], matrix[1] = matrix[1], matrix[0]
        self.assertEqual(calculate_determinant(matrix), 24)

    def test_large_integers(self):
        value = 10**30
        matrix = [[value, value - 1], [value + 1, value]]
        self.assertEqual(calculate_determinant(matrix), 1)

    def test_matrix_is_not_modified(self):
        matrix = [[2, 1, 3], [0, -1, 4], [5, 2, 0]]
        original = [row[:] for row in matrix]
        self.assertEqual(calculate_determinant(matrix), 19)
        self.assertEqual(matrix, original)

    def test_generator(self):
        """Проверяет генератор матриц с известным определителем"""
        require_generator(self)
        for order in range(1, 6):
            with self.subTest(order=order):
                test_case = generate_matrix_and_det(order)
                self.assertEqual(len(test_case.matrix), order)
                for row in test_case.matrix:
                    self.assertEqual(len(row), order)
                self.assertEqual(calculate_determinant(test_case.matrix), test_case.det)


if __name__ == "__main__":
    unittest.main()
