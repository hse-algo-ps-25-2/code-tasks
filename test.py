import math
import unittest

from main import generate_permutations_iter, generate_permutations_rec


def _same_items(left, right):
    pending = list(right)
    for item in left:
        for index, candidate in enumerate(pending):
            if candidate == item:
                del pending[index]
                break
        else:
            return False
    return not pending


def _assert_all_permutations(test_case, permutations, elements):
    test_case.assertIsInstance(permutations, list)
    test_case.assertEqual(len(permutations), math.factorial(len(elements)))
    seen = []
    for permutation in permutations:
        test_case.assertIsInstance(permutation, list)
        test_case.assertTrue(_same_items(permutation, elements))
        snapshot = list(permutation)
        test_case.assertNotIn(snapshot, seen)
        seen.append(snapshot)


class TestPermutations(unittest.TestCase):
    """Публичные примеры генерации перестановок."""

    def test_two_letters(self):
        """Обе перестановки двух букв."""
        expected = [["a", "b"], ["b", "a"]]
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                self.assertTrue(_same_items(function(["a", "b"]), expected))

    def test_three_letters(self):
        """Все шесть перестановок трёх букв."""
        elements = ["a", "b", "c"]
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                _assert_all_permutations(self, function(elements), elements)

    def test_empty_list(self):
        """У пустого списка одна пустая перестановка"""
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                self.assertEqual(function([]), [[]])

    def test_single_element(self):
        """Единственный элемент образует одну перестановку"""
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                self.assertEqual(function([42]), [[42]])

    def test_four_numbers(self):
        """Все 24 перестановки четырёх чисел"""
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                elements = [-7, -11, 25, 2]
                permutations = function(list(elements))
                _assert_all_permutations(self, permutations, elements)

    def test_mixed_objects(self):
        """Корректно обрабатываются элементы разных типов"""
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                for elements in (
                    [None, 67, 1.2, "строка"],
                    [[2, "3"], (None, 0.0), {"value": 3}, object()],
                ):
                    with self.subTest(function=function.__name__, elements=elements):
                        permutations = function(list(elements))
                        _assert_all_permutations(self, permutations, elements)

    def test_duplicate_elements(self):
        """Повторяющиеся элементы вызывают ValueError"""
        for function in (generate_permutations_rec, generate_permutations_iter):
            for elements in ([1, 1], [1, 2, 1], [(1, 2), (1, 2)], [None, None]):
                with self.subTest(function=function.__name__, elements=elements):
                    with self.assertRaises(ValueError):
                        function(elements)

    def test_false_duplicate_elements(self):
        """Сравнимые, но разные элементы не вызывают ValueError"""
        for function in (generate_permutations_rec, generate_permutations_iter):
            for elements in ([1, True], [1, 1.0]):
                with self.subTest(function=function.__name__, elements=elements):
                    permutations = function(list(elements))
                    _assert_all_permutations(self, permutations, elements)

    def test_non_list_argument(self):
        """Любой аргумент, не являющийся списком, вызывает TypeError."""
        for function in (generate_permutations_rec, generate_permutations_iter):
            for invalid_argument in (
                None,
                True,
                False,
                42,
                3.14,
                "строка",
                (1, 2),
                {"value": 1},
                {1, 2},
                range(2),
                iter([1, 2]),
            ):
                with self.subTest(
                    function=function.__name__,
                    argument_type=type(invalid_argument).__name__,
                    argument=invalid_argument,
                ):
                    with self.assertRaises(TypeError):
                        function(invalid_argument)


if __name__ == "__main__":
    unittest.main()
