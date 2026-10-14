import unittest

from main import (
    LENGTH_NOT_INT,
    LENGTH_NOT_POS,
    N_LESS_THAN_K_ERROR_MSG,
    NEGATIVE_VALUE_TEMPL,
    NOT_INT_VALUE_TEMPL,
    binomial_coefficient_iter,
    binomial_coefficient_rec,
    generate_strings,
)
from strings_checker import check_strings

BINOMIAL_FUNCTIONS = (binomial_coefficient_iter, binomial_coefficient_rec)
WRONG_TYPES = ["2", 2.5, None, True]


class TestZeroOne(unittest.TestCase):
    """Набор тестов генерации строк"""

    def test_valid_lengths(self):
        """Длины от 1 до 8 проходят проверку полноты"""
        for length in range(1, 9):
            with self.subTest(length=length):
                self.assertTrue(check_strings(generate_strings(length), length))

    def test_length_three_exact(self):
        """Длина 3: ровно пять ожидаемых строк"""
        expected = {"111", "110", "101", "011", "010"}
        self.assertEqual(set(generate_strings(3)), expected)

    def test_count_is_fibonacci(self):
        """Количество строк длины n равно F(n+2), без повторов"""
        fib = [1, 2]
        for _ in range(8):
            fib.append(fib[-1] + fib[-2])
        for length in range(1, 9):
            with self.subTest(length=length):
                result = generate_strings(length)
                self.assertEqual(len(result), fib[length])
                self.assertEqual(len(set(result)), len(result))

    def test_length_not_int(self):
        """Длина не целое"""
        for value in ["1", 1.0, 2.5, None, True]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as error:
                    generate_strings(value)
                self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_not_positive(self):
        """Длина меньше единицы: ноль и отрицательные"""
        for value in [0, -1, -10]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as error:
                    generate_strings(value)
                self.assertEqual(str(error.exception), LENGTH_NOT_POS)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_known_values(self):
        """Известные значения у обеих функций"""
        cases = [((5, 2), 10), ((6, 3), 20), ((10, 4), 210), ((4, 1), 4)]
        for func in BINOMIAL_FUNCTIONS:
            for args, expected in cases:
                with self.subTest(func=func.__name__, args=args):
                    self.assertEqual(func(*args), expected)

    def test_base_cases(self):
        """C(n, 0) = C(n, n) = 1, включая C(0, 0)"""
        for func in BINOMIAL_FUNCTIONS:
            for n, k in [(0, 0), (1, 0), (1, 1), (10, 0), (10, 10)]:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), 1)

    def test_functions_agree(self):
        """Итеративная и рекурсивная версии дают одинаковый результат"""
        for n in range(0, 12):
            for k in range(0, n + 1):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        binomial_coefficient_iter(n, k),
                        binomial_coefficient_rec(n, k),
                    )

    def test_symmetry(self):
        """C(n, k) = C(n, n - k)"""
        for func in BINOMIAL_FUNCTIONS:
            for n, k in [(8, 3), (9, 2), (10, 7)]:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), func(n, n - k))

    def test_large_value_iter(self):
        """Большие значения считает итеративная версия"""
        self.assertEqual(binomial_coefficient_iter(30, 20), 30045015)

    def test_n_less_than_k(self):
        """n меньше k"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(1, 2)
                self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_n_not_int(self):
        """n не целое"""
        for func in BINOMIAL_FUNCTIONS:
            for value in WRONG_TYPES:
                with self.subTest(func=func.__name__, n=value):
                    with self.assertRaises(TypeError) as error:
                        func(value, 1)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("n")
                    )

    def test_k_not_int(self):
        """k не целое"""
        for func in BINOMIAL_FUNCTIONS:
            for value in WRONG_TYPES:
                with self.subTest(func=func.__name__, k=value):
                    with self.assertRaises(TypeError) as error:
                        func(1, value)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("k")
                    )

    def test_negative_params(self):
        """Отрицательные n и k"""
        cases = [((-1, 2), "n"), ((10, -2), "k"), ((-3, -1), "n")]
        for func in BINOMIAL_FUNCTIONS:
            for args, name in cases:
                with self.subTest(func=func.__name__, args=args):
                    with self.assertRaises(TypeError) as error:
                        func(*args)
                    self.assertEqual(
                        str(error.exception), NEGATIVE_VALUE_TEMPL.format(name)
                    )


if __name__ == "__main__":
    unittest.main()
