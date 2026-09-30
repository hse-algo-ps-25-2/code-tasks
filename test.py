import unittest
from itertools import permutations

from main import get_tridiagonal_determinant


class TestTridiagonalDeterminant(unittest.TestCase):
    """Набор тестов для проверки функции вычисления определителя
    трёхдиагональной ленточной матрицы"""

    def test_invalid_structure(self):
        for matrix in [42, "matrix", (1,), [1], [[1], None], [[1, 2], [3]]]:
            with self.subTest(matrix=matrix), self.assertRaises(Exception):
                get_tridiagonal_determinant(matrix)

    def test_non_integer_elements(self):
        for matrix in [[[1.5]], [["1"]], [[None]], [[1, 2.5], [3, 1]]]:
            with self.subTest(matrix=matrix), self.assertRaises(Exception):
                get_tridiagonal_determinant(matrix)

    def test_non_constant_diagonals(self):
        matrices = [
            [[1, 2], [3, 4]],
            [[1, 2, 0], [3, 1, 4], [0, 3, 1]],
            [[1, 2, 0], [3, 1, 2], [0, 4, 1]],
        ]
        for matrix in matrices:
            with self.subTest(matrix=matrix), self.assertRaises(Exception):
                get_tridiagonal_determinant(matrix)

    def test_nonzero_below_band(self):
        matrix = [[1, 2, 0], [3, 1, 2], [7, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_against_permutation_definition(self):
        # Независимая проверка по определению определителя, без рекурсии.
        for n in range(1, 7):
            for a, b, c in [
                (0, 0, 0),
                (0, 2, 3),
                (-2, 3, -4),
                (3, 0, 2),
                (3, 2, 0),
                (10**20, 1, -1),
            ]:
                matrix = [
                    [
                        a if i == j else b if j == i + 1 else c if i == j + 1 else 0
                        for j in range(n)
                    ]
                    for i in range(n)
                ]
                original = [row[:] for row in matrix]
                expected = 0
                for permutation in permutations(range(n)):
                    inversions = sum(
                        permutation[i] > permutation[j]
                        for i in range(n)
                        for j in range(i + 1, n)
                    )
                    product = 1
                    for i, j in enumerate(permutation):
                        product *= matrix[i][j]
                    expected += (-1) ** inversions * product
                with self.subTest(n=n, a=a, b=b, c=c):
                    self.assertEqual(get_tridiagonal_determinant(matrix), expected)
                    self.assertEqual(matrix, original)

    def test_repeated_calls(self):
        for matrix, expected in [
            ([[2, 1, 0], [1, 2, 1], [0, 1, 2]], 4),
            ([[3, 1, 0], [1, 3, 1], [0, 1, 3]], 21),
            ([[2, 1, 0], [1, 2, 1], [0, 1, 2]], 4),
        ]:
            with self.subTest(matrix=matrix):
                self.assertEqual(get_tridiagonal_determinant(matrix), expected)

    def test_larger_matrix(self):
        n = 100
        matrix = [
            [2 if i == j else -1 if abs(i - j) == 1 else 0 for j in range(n)]
            for i in range(n)
        ]
        self.assertEqual(get_tridiagonal_determinant(matrix), n + 1)

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


if __name__ == "__main__":
    unittest.main()
