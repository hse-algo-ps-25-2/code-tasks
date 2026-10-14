import unittest

from main import (
    LENGTH_NOT_INT,
    N_LESS_THAN_K_ERROR_MSG,
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

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_one(self):
        self.assertEqual(set(generate_strings(1)), {"0", "1"})

    def test_length_three(self):
        self.assertTrue(check_strings(generate_strings(3), 3))

    def test_length_zero(self):
        with self.assertRaises(ValueError):
            generate_strings(0)

    def test_length_bool(self):
        with self.assertRaises(TypeError):
            generate_strings(True)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_n_less_than_k(self):
        """n меньше k"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_iter(1, 2)
        self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_n_is_not_int(self):
        """n не целое"""
        with self.assertRaises(TypeError) as error:
            binomial_coefficient_rec("a", 2)
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))

    def test_zero_both(self):
        self.assertEqual(binomial_coefficient_iter(0, 0), 1)
        self.assertEqual(binomial_coefficient_rec(0, 0), 1)

    def test_edges_both(self):
        self.assertEqual(binomial_coefficient_iter(5, 0), 1)
        self.assertEqual(binomial_coefficient_rec(5, 5), 1)

    def test_negative_k(self):
        with self.assertRaises(ValueError):
            binomial_coefficient_iter(5, -1)

        with self.assertRaises(ValueError):
            binomial_coefficient_rec(5, -1)


if __name__ == "__main__":
    unittest.main()
