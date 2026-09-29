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

    def test_fifth_order(self):
        """Проверяет расчет определителя для матрицы порядка 5"""
        matrix = [
            [1, -3, 4, 2, 0],
            [6, 2, -5, -1, 1],
            [4, 2, 7, 3, -3],
            [5, 3, 1, 7, 0],
            [1, 4, -2, -1, 5],
        ]
        self.assertEqual(calculate_determinant(matrix), 8302)

    def test_sixth_order(self):
        """Проверяет расчет определителя для матрицы порядка 6"""
        matrix = [
            [3, -5, 0, 7, -2, 4],
            [-7, 1, 6, -3, 5, -1],
            [2, 0, -4, 7, -6, 3],
            [5, -2, 1, -7, 0, 6],
            [-3, 4, -5, 2, 7, -1],
            [6, -6, 3, 0, -4, 5],
        ]
        self.assertEqual(calculate_determinant(matrix), -10357)

    def test_seventh_order(self):
        """Проверяет расчет определителя для матрицы порядка 7"""
        matrix = [
            [1, -2, 3, -1, 2, -3, 4],
            [-3, 2, -1, 3, -2, 1, -5],
            [2, -1, 3, -2, 1, -3, 2],
            [-1, 3, -2, 1, -3, 6, -1],
            [3, -3, 1, -1, 2, -2, 3],
            [-2, 1, -3, 2, -4, 3, -1],
            [1, -2, 2, -3, 1, -1, 2],
        ]
        self.assertEqual(calculate_determinant(matrix), -2064)

    def test_eighth_order(self):
        """Проверяет расчет определителя для матрицы порядка 8"""
        matrix = [
            [1, -2, 3, 0, 2, -3, 1, -1],
            [-3, 2, -1, 3, -2, 4, -2, 1],
            [2, -1, 3, -2, 0, -3, 2, 3],
            [-1, 3, -2, 1, -3, 1, -5, 2],
            [3, -3, 1, -1, 2, -2, 3, 0],
            [-2, 1, -3, 2, -1, 3, -1, 6],
            [1, -2, 2, -3, 1, -1, 2, -3],
            [2, 1, -1, 3, -2, 0, -3, 1],
        ]
        self.assertEqual(calculate_determinant(matrix), -544)

    def test_ninth_order(self):
        """Проверяет расчет определителя для матрицы порядка 9"""
        matrix = [
            [1, -1, -3, 3, -6, 1, 3, -3, 1],
            [2, 5, 0, 2, 1, 0, -3, -2, 3],
            [1, 4, 2, 3, 1, 3, -3, -2, 2],
            [2, -1, -3, -2, -2, 2, 3, 2, 3],
            [3, -4, -1, 1, -6, 1, 4, -3, 0],
            [-3, 1, 3, -2, -6, -3, 1, -6, -3],
            [1, 4, 1, -1, 2, -3, 1, 3, 2],
            [5, -4, 1, 2, -3, -2, 6, 6, -3],
            [2, 5, 0, 2, 5, -1, 2, 2, 3],
        ]
        self.assertEqual(calculate_determinant(matrix), -1417997)

    def test_tenth_order(self):
        """Проверяет расчет определителя для матрицы порядка 10"""
        matrix = [
            [0, 1, 1, -2, 0, 3, 2, -3, 1, -1],
            [2, 5, 6, -5, 3, 2, 1, -2, 2, 1],
            [2, 2, -3, 3, 6, 6, 2, -5, -6, -3],
            [5, -2, -1, 3, -1, 1, 1, -4, 1, 3],
            [-3, -2, -1, -5, 1, 3, 2, 1, 3, -3],
            [1, -1, 2, 0, 3, -3, 0, 3, 5, 1],
            [-1, 2, -2, 2, -3, -3, 1, -3, 2, 3],
            [3, 1, -1, 1, -6, 2, -1, -1, -3, 1],
            [1, -1, 3, 2, -2, 1, 4, 1, 2, -4],
            [1, 1, -1, -1, 1, 1, 1, -3, 1, 6],
        ]
        self.assertEqual(calculate_determinant(matrix), 6993172)

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
