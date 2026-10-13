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
WRONG_TYPE_VALUES = ["2", 2.5, None, True]


class TestZeroOne(unittest.TestCase):
    """Набор тестов генерации строк"""

    def test_length_one(self):
        """Длина 1"""
        self.assertTrue(check_strings(generate_strings(1), 1))

    def test_length_two(self):
        """Длина 2"""
        self.assertTrue(check_strings(generate_strings(2), 2))

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_three(self):
        """Длина 3"""
        self.assertTrue(check_strings(generate_strings(3), 3))

    def test_length_four(self):
        """Длина 4"""
        self.assertTrue(check_strings(generate_strings(4), 4))

    def test_length_five(self):
        """Длина 5"""
        self.assertTrue(check_strings(generate_strings(5), 5))

    def test_length_not_pos(self):
        """Длина не меньше единицы"""
        with self.assertRaises(ValueError) as error:
            generate_strings(-1)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_not_pos_zero(self):
        """Длина не меньше единицы, ноль"""
        with self.assertRaises(ValueError) as error:
            generate_strings(0)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_not_int(self):
        """Длина не целое"""
        cases = ["1", 1.0, None, True]
        for case_value in cases:
            with self.assertRaises(TypeError) as error:
                generate_strings(case_value)
            self.assertEqual(str(error.exception), LENGTH_NOT_INT)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_base_cases(self):
        """базовые случаи"""
        cases = [[0, 0], [1, 0], [1, 1], [10, 0], [10, 10]]
        for func in BINOMIAL_FUNCTIONS:
            for n, k in cases:
                with self.subTest(func=func.__name__):
                    self.assertEqual(func(n, k), 1)

    def test_n_is_less_than_k(self):
        """n меньше k"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(1, 2)
                self.assertEqual(N_LESS_THAN_K_ERROR_MSG, str(error.exception))

    def test_n_is_not_int(self):
        """n не является целым"""
        for func in BINOMIAL_FUNCTIONS:
            for case_value in WRONG_TYPE_VALUES:
                with self.subTest(func=func.__name__, n=case_value):
                    with self.assertRaises(TypeError) as error:
                        func(case_value, 1)
                    self.assertEqual(
                        NOT_INT_VALUE_TEMPL.format("n"), str(error.exception)
                    )
    
    def test_k_is_not_int(self):
        """k не является целым"""
        for func in BINOMIAL_FUNCTIONS:
            for case_value in WRONG_TYPE_VALUES:
                with self.subTest(func=func.__name__, k=case_value):
                    with self.assertRaises(TypeError) as error:
                        func(1, case_value)
                    self.assertEqual(
                        NOT_INT_VALUE_TEMPL.format("k"), str(error.exception)
                    )

    def test_n_is_negative(self):
        """n отрицательное число"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(-1, 2)
                self.assertEqual(NEGATIVE_VALUE_TEMPL.format("n"), str(error.exception))

    def test_k_is_negative(self):
        """k отрицательное число"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(10, -2)
                self.assertEqual(NEGATIVE_VALUE_TEMPL.format("k"), str(error.exception))


if __name__ == "__main__":
    unittest.main()
