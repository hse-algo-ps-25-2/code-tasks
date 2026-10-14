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


class TestZeroOne(unittest.TestCase):
    """Набор тестов генерации строк"""

    def test_length_two(self):
        """Длина 2"""
        self.assertTrue(check_strings(generate_strings(2), 2))

    def test_several_lengths(self):
        """Полнота набора для нескольких длин"""
        for length in (1, 3, 5, 10):
            with self.subTest(length=length):
                self.assertTrue(check_strings(generate_strings(length), length))

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_pos(self):
        """Длина меньше единицы"""
        for bad in (0, -1):
            with self.subTest(length=bad):
                with self.assertRaises(ValueError) as error:
                    generate_strings(bad)
                self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_bool(self):
        """Длина булева"""
        with self.assertRaises(TypeError) as error:
            generate_strings(True)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_generated_property(self):
        """Длина 5: нет двух нулей подряд, количество совпадает с F(7)"""
        strings = generate_strings(5)
        for s in strings:
            self.assertNotIn("00", s)
        self.assertEqual(len(strings), 13)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_n_less_than_k(self):
        """n меньше k"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(1, 2)
                self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_n_is_not_int(self):
        """n не целое"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func("a", 2)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))

    def test_bool_args(self):
        """bool не считается целым"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(True, 1)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))

    def test_negative_args(self):
        """Отрицательные n и k"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__, param="n"):
                with self.assertRaises(ValueError) as error:
                    func(-1, 0)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))
            with self.subTest(func=func.__name__, param="k"):
                with self.assertRaises(ValueError) as error:
                    func(5, -1)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))

    def test_binomial_boundary(self):
        """C(n, 0) = C(n, n) = 1 для обеих реализаций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(0, 0), 1)
                self.assertEqual(func(5, 0), 1)
                self.assertEqual(func(5, 5), 1)

    def test_agreement(self):
        """Обе реализации согласованы на нескольких значениях"""
        for n, k in [(0, 0), (3, 1), (5, 2), (10, 5), (15, 7)]:
            with self.subTest(n=n, k=k):
                self.assertEqual(
                    binomial_coefficient_iter(n, k),
                    binomial_coefficient_rec(n, k),
                )


if __name__ == "__main__":
    unittest.main()
