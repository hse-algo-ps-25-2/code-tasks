import unittest
from typing import ClassVar

from main import fibonacci, fibonacci_iter, fibonacci_rec


class TestFibonacci(unittest.TestCase):
    """Тесты для проверки функций вычисления числа Фибоначчи"""

    fibonacci_numbers: ClassVar[list[int]] = [
        1,
        1,
        2,
        3,
        5,
        8,
        13,
        21,
        34,
        55,
        89,
        144,
        233,
        377,
        610,
        987,
        1597,
        2584,
        4181,
        6765,
        10946,
        17711,
    ]

    def test_fibonacci_rec(self):
        """Проверка работы рекурсивной функции вычисления числа Фибоначчи"""

        for n, expected in enumerate(self.fibonacci_numbers, start=1):
            with self.subTest(n=n):
                assert fibonacci_rec(n) == expected

    def test_fibonacci_iter(self):
        """Проверка работы итеративной функции вычисления числа Фибоначчи"""

        for n, expected in enumerate(self.fibonacci_numbers, start=1):
            with self.subTest(n=n):
                assert fibonacci_iter(n) == expected

    def test_fibonacci(self):
        """Проверка работы итеративной функции вычисления числа Фибоначчи
        без использования массива"""

        for n, expected in enumerate(self.fibonacci_numbers, start=1):
            with self.subTest(n=n):
                assert fibonacci(n) == expected


if __name__ == "__main__":
    unittest.main()
