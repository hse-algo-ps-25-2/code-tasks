import unittest

from main import get_tridiagonal_determinant


class TestTridiagonalDeterminant(unittest.TestCase):
    """Набор тестов для проверки функции вычисления определителя
    трёхдиагональной ленточной матрицы"""

    def test_none(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения None"""
        self.assertRaises(Exception, get_tridiagonal_determinant, None)

    def test_empty_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого списка"""
        self.assertRaises(Exception, get_tridiagonal_determinant, [])

    def test_not_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы"""
        matrix = [[1, 2, 0, 0], [3, 1, 2, 0], [0, 3, 1, 2]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_not_tridiag_replace_zero(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы с ненулевым элементом вне трёх диагоналей"""
        matrix = [[1, 2, 0, 7], [3, 1, 2, 0], [0, 3, 1, 2], [0, 0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_first_order(self):
        """Проверяет расчет определителя для матрицы порядка 1"""
        matrix = [[1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 1)

    def test_second_order(self):
        """Проверяет расчет определителя для матрицы порядка 2"""
        matrix = [[1, 2], [2, 1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -3)

    def test_third_order(self):
        """Проверяет расчет определителя для матрицы порядка 3"""
        matrix = [[1, -2, 0], [-4, 1, -2], [0, -4, 1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -15)

    def test_fourth_order(self):
        """Проверяет расчет определителя для матрицы порядка 4"""
        matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 421)


    def test_is_list_number(self):
        self.assertRaises(Exception, get_tridiagonal_determinant, 11)

    def test_is_list_str(self):
        self.assertRaises(Exception, get_tridiagonal_determinant, "hello")

    def test_is_list_tuple(self):
        self.assertRaises(Exception, get_tridiagonal_determinant, ((1, 2), (2, 1)))

    def test_is_row_list_tuple(self):
        self.assertRaises(Exception, get_tridiagonal_determinant, [(1, 2), (2, 1)])

    def test_is_row_list_str(self):
        self.assertRaises(Exception, get_tridiagonal_determinant, [["hi", "hey"], ["hey", "hi"]])

    def test_float(self):
        self.assertRaises(Exception, get_tridiagonal_determinant, [[1.0, 2.0], [2.0, 1.0]])

    def test_bool(self):
        self.assertRaises(Exception, get_tridiagonal_determinant, [[True, False], [False, True]])

    def test_main_diagonal_inconsistent(self):
        matrix = [[1, -2, 0], [-4, 9, -2], [0, -4, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_top_diagonal_inconsistent(self):
        matrix = [[1, -2, 0], [-4, 1, 9], [0, -4, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_bottom_diagonal_inconsistent(self):
        matrix = [[1, -2, 0], [9, 1, -2], [0, -4, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)
        
    def test_zero(self):
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)

    def test_one(self):
            matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            self.assertEqual(get_tridiagonal_determinant(matrix), 1)


if __name__ == "__main__":
    unittest.main()
