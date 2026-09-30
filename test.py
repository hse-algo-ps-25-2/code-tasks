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

    def test_boolean(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения типа boolean"""
        self.assertRaises(Exception, calculate_determinant, False)

    def test_string(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения типа string"""
        self.assertRaises(Exception, calculate_determinant, "matrix")

    def test_int(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения типа int"""
        self.assertRaises(Exception, calculate_determinant, 1)

    def test_float(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения типа float"""
        self.assertRaises(Exception, calculate_determinant, 3.14)

    def test_tuple(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого кортежа"""
        self.assertRaises(Exception, calculate_determinant, ())

    def test_dict(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого словаря"""
        self.assertRaises(Exception, calculate_determinant, {})

    def test_empty_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого списка"""
        self.assertRaises(Exception, calculate_determinant, [])

    def test_empty_row_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы с пустой строкой"""
        self.assertRaises(Exception, calculate_determinant, [[]])

    def test_not_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы"""
        matrix = [[3, -3, -5, 8], [-3, 2, 4, -6], [-4, 3, 5, -6]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_invalid_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы с разным количеством элементов в строках"""
        matrix = [[3, -3, -5], [-3, 2, 4], [-4, 3]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_empty_element_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы с пустым элементом"""
        matrix = [[1, 2], [1, None]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_boolean_element_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы с элементом типа boolean"""
        matrix = [[1, 2], [1, False]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_string_element_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы со строковым элементом"""
        matrix = [[1, 2], [3, "4"]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_float_element_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр матрицы с элементом типа float"""
        matrix = [[1, 2], [1, 3.14]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_first_order(self):
        """Проверяет расчет определителя для матрицы порядка 1"""
        matrix = [[1]]
        self.assertEqual(calculate_determinant(matrix), 1)

    def test_zero_matrix_third_order(self):
        """Проверяет расчет определителя для нулевой матрицы 3-го порядка."""
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self.assertEqual(calculate_determinant(matrix), 0)

    def test_identity_matrix(self):
        """Проверяет расчет определителя для единичной матрицы."""
        matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        self.assertEqual(calculate_determinant(matrix), 1)

    def test_diagonal_matrix(self):
        """Проверяет расчет определителя для диагональной матрицы."""
        matrix = [[2, 0, 0], [0, 3, 0], [0, 0, 4]]

        self.assertEqual(calculate_determinant(matrix), 24)

    def test_triangular_matrix(self):
        """Проверяет расчет определителя для треугольной матрицы."""
        matrix = [[2, 5, 7], [0, 3, 4], [0, 0, 6]]

        self.assertEqual(calculate_determinant(matrix), 36)

    def test_equal_rows(self):
        """Проверяет расчет определителя для матрицы с двумя одинаковыми строками."""
        matrix = [[1, 2, 3], [4, 5, 6], [1, 2, 3]]

        self.assertEqual(calculate_determinant(matrix), 0)

    def test_second_order(self):
        """Проверяет расчет определителя для матрицы порядка 2"""
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(calculate_determinant(matrix), -2)

    def test_zero_matrix(self):
        """Проверяет расчет определителя для нулевой матрицы."""
        matrix = [[0, 0], [0, 0]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_third_order(self):
        """Проверяет расчет определителя для матрицы порядка 3"""
        matrix = [[1, -2, 3], [-4, 5, -6], [7, -8, 9]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_fourth_order(self):
        """Проверяет расчет определителя для матрицы порядка 4"""
        matrix = [[3, -3, -5, 8], [-3, 2, 4, -6], [2, -5, -7, 5], [-4, 3, 5, -6]]
        self.assertEqual(calculate_determinant(matrix), 18)

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
