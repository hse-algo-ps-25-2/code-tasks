import random
import unittest

from constants import Exceptions
from main import recursive_sort


class TestRecursiveSort(unittest.TestCase):
    """Набор тестов рекурсивной сортировки"""

    def test_empty(self):
        """Пустой список"""
        assert recursive_sort([]) == []

    def test_one(self):
        """Проверка для одного значения"""
        assert recursive_sort([1]) == [1]

    def test_two(self):
        """Два элемента"""
        assert recursive_sort([2, 1]) == [1, 2]

    def test_random(self):
        """Множество случайных значений"""
        randomized_values = [random.randint(1, 100) for _ in range(100)]
        assert recursive_sort(randomized_values) == sorted(randomized_values)

    def test_not_list(self):
        """Набор не список"""
        with self.assertRaises(TypeError) as error:
            recursive_sort(1)
        assert str(error.exception) == Exceptions.NOT_LIST

    def test_with_duplicates(self):
        """Много дубликатов"""
        data = [3, 1, 3, 2, 1, 3, 2, 1]
        assert recursive_sort(data) == sorted(data)

    def test_returns_new_list(self):
        """Возвращается новый список, исходный не меняется"""
        data = [3, 1, 2]
        result = recursive_sort(data)
        assert result is not data
        assert data == [3, 1, 2]
        assert result == [1, 2, 3]

    def test_returns_new_list_single(self):
        """Даже для одноэлементного списка возвращается копия"""
        data = [42]
        result = recursive_sort(data)
        assert result is not data
        assert result == [42]

    def test_incomparable(self):
        """Несравнимые элементы"""
        with self.assertRaises(TypeError) as error:
            recursive_sort([1, "a"])
        assert str(error.exception) == Exceptions.NOT_COMPARABLE

    def test_odd_length(self):
        """Нечётное количество элементов"""
        data = [5, 3, 8, 1, 9, 2, 7]
        assert recursive_sort(data) == sorted(data)


if __name__ == "__main__":
    unittest.main()
