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

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)


    def test_length_one(self):
        """Длина 1"""
        self.assertEqual(sorted(generate_strings(1)), ["0", "1"])

    def test_length_five(self):
        """Длины 5"""
        self.assertTrue(check_strings(generate_strings(5), 5))

    def test_length_bool(self):
        """Длина не булево значение"""
        with self.assertRaises(TypeError) as error:
            generate_strings(True)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_zero(self):
        """Длина не 0"""
        with self.assertRaises(ValueError) as error:
            generate_strings(0)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_negative(self):
        """Длина не отрицательное значение"""
        with self.assertRaises(ValueError) as error:
            generate_strings(-2)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)        

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


    def test_k_is_not_int(self):
        """k не целое"""
        with self.assertRaises(TypeError) as error:
            binomial_coefficient_rec(2, 1.2)
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_n_is_bool(self):
        """n не булево значение"""
        with self.assertRaises(TypeError) as error:
            binomial_coefficient_rec(True, 2)
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))

    def test_k_is_bool(self):
        """k не булево значение"""
        with self.assertRaises(TypeError) as error:
            binomial_coefficient_rec(2, False)
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_n_is_negative(self):
        """n не отрицательное значение"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_rec(-1, 2)
        self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))

    def test_k_is_negative(self):
        """k не отрицательное значение"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_rec(2, -1)
        self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))

    def test_k_equals_n(self):
        """C(n, n) = 1"""
        n = 5
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(n, n), 1)

    def test_k_equals_n(self):
        """C(n, 0) = 1"""
        n = 5
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(n, 0), 1)

    def test_both_zero(self):
            """C(0, 0) = 1"""
            for func in BINOMIAL_FUNCTIONS:
                with self.subTest(func=func.__name__):
                    self.assertEqual(func(0, 0), 1)

    def test_iter_equals_rec(self):
        """Обе функции дают одинаковый результат"""
        n, k = 5, 3
        self.assertEqual(binomial_coefficient_iter(n, k), binomial_coefficient_rec(n, k))

    def test_symmetry(self):
        """C(n, k) = C(n, n - k)"""
        n = 5
        k = 3
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(n, k), func(n, n - k))


if __name__ == "__main__":
    unittest.main()
