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

    def test_three_strings(self):
        elements = ["c", "a", "b"]
        expected = [
            ["a", "b", "c"],
            ["a", "c", "b"],
            ["b", "a", "c"],
            ["b", "c", "a"],
            ["c", "a", "b"],
            ["c", "b", "a"],
        ]
        assert_lex(self, elements, expected)
        self.assertEqual(elements, ["c", "a", "b"])

    def test_repeated_elements(self):
        assert_lex(self, [2, 1, 1], [[1, 1, 2], [1, 2, 1], [2, 1, 1]])

    def test_requires_list(self):
        for value in (True, "ab", (1, 2)):
            with self.subTest(value=value), self.assertRaises(TypeError):
                list(generate_permutations(value))


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

    def test_shortest_cycle(self):
        matrix = [[None, 5, 2], [4, None, 6], [7, 3, None]]
        solver = BruteForceTspSolver(matrix)
        self.assertEqual(solver.get_tsp_solution(), TspSolution(9, [0, 2, 1, 0]))

    def test_missing_and_free_edges(self):
        matrix = [[None, 0, None], [None, None, 0], [0, None, None]]
        solver = BruteForceTspSolver(matrix)
        self.assertEqual(solver.get_tsp_solution(), TspSolution(0, [0, 1, 2, 0]))

    def test_wrong_matrix(self):
        matrices = ([[None, 1], [2]], [[None, 1], None], [[None, "x"], [2, None]])
        for matrix in matrices:
            with self.subTest(matrix=matrix):
                with self.assertRaises(TypeError) as error:
                    BruteForceTspSolver(matrix)
                self.assertEqual(str(error.exception), ErrorMessageEnum.WRONG_MATRIX)

    def test_negative_distance(self):
        with self.assertRaises(ValueError) as error:
            BruteForceTspSolver([[None, 1], [-2, None]])
        self.assertEqual(str(error.exception), ErrorMessageEnum.NEG_VALUE)


if __name__ == "__main__":
    unittest.main()
