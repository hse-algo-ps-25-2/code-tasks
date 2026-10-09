import unittest

from main import NOT_LIST, recursive_sort


class TestRecursiveSort(unittest.TestCase):
    """Набор тестов рекурсивной сортировки"""

    def test_empty(self):
        """Пустой список"""
        self.assertEqual(recursive_sort([]), [])

    def test_two(self):
        """Два элемента"""
        self.assertEqual(recursive_sort([2, 1]), [1, 2])

    def test_not_list(self):
        """Набор не список"""
        with self.assertRaises(TypeError) as error:
            recursive_sort(1)
        self.assertEqual(str(error.exception), NOT_LIST)


if __name__ == "__main__":
    unittest.main()
