import unittest

from main import NOT_LIST_ERROR_MESSAGE, recursive_quicksort


class TestRecursiveSort(unittest.TestCase):
    """Набор тестов рекурсивной сортировки"""

    def test_empty(self):
        """Пустой список"""
        self.assertEqual(recursive_quicksort([]), [])

    def test_two(self):
        """Два элемента"""
        self.assertEqual(recursive_quicksort([2, 1]), [1, 2])

    def test_items_list_from_example(self):
        "items из примера"

        self.assertEqual(\
            recursive_quicksort(\
                [5, 8, 1, 4, -7, 6, 12, 19, -6]),\
                    [-7, -6, 1, 4, 5, 6, 8, 12, 19])

    def test_not_list(self):
        """Правильный TypeError если items не список"""
        with self.assertRaises(TypeError) as error:
            recursive_quicksort(1)
        self.assertEqual(str(error.exception), NOT_LIST_ERROR_MESSAGE)


if __name__ == "__main__":
    unittest.main()
