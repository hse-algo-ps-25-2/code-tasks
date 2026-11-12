import unittest
from collections.abc import Generator

from brute_force_tsp_solver import BruteForceTspSolver
from error_message_enum import ErrorMessageEnum
from permutation_generator import generate_permutations
from tsp_abs_solver import TspSolution


def assert_lex(test, elements, expected):
    """Генератор выдаёт перестановки в лексикографическом порядке"""
    result = generate_permutations(elements)
    test.assertIsInstance(result, Generator)
    test.assertEqual(list(result), expected)


class TestPermutationGenerator(unittest.TestCase):
    """Примеры генератора перестановок"""

    def test_empty(self):
        """Пустой список даёт одну пустую перестановку"""
        assert_lex(self, [], [[]])

    def test_single_num(self):
        """Один элемент даёт одну перестановку"""
        assert_lex(self, [1], [[1]])

    def test_double_num(self):
        """Два числа идут в лексикографическом порядке"""
        assert_lex(self, [2, 1], [[1, 2], [2, 1]])


class TestTsp(unittest.TestCase):
    """Примеры полного перебора коммивояжёра"""

    def test_not_a_list(self):
        """Орграф передают матрицей"""
        self.assertRaisesRegex(
            TypeError,
            ErrorMessageEnum.WRONG_MATRIX,
            BruteForceTspSolver,
            None,
        )

    def test_single(self):
        """Один город уже является маршрутом длины 0"""
        solver = BruteForceTspSolver([[None]])
        self.assertEqual(solver.get_tsp_solution(), TspSolution(0, [0]))

    def test_distance(self):
        """Длина маршрута — сумма последовательных рёбер"""
        matrix = [[None, 1.0], [2.0, None]]
        solver = BruteForceTspSolver(matrix)
        self.assertEqual(solver.get_distance(matrix, [0, 1, 0]), 3)
        self.assertEqual(solver.get_distance([[None]], [0]), 0)

    def test_double(self):
        """Два города: маршрут возвращается в начало"""
        matrix = [[None, 1.0], [2.0, None]]
        solver = BruteForceTspSolver(matrix)
        self.assertEqual(solver.get_tsp_solution(), TspSolution(3, [0, 1, 0]))

    def test_has_not_path(self):
        """Если цикла нет, расстояние пусто и маршрут пуст"""
        matrix = [[None, 1.0], [None, None]]
        solver = BruteForceTspSolver(matrix)
        self.assertEqual(solver.get_tsp_solution(), TspSolution(None, []))


if __name__ == "__main__":
    unittest.main()
