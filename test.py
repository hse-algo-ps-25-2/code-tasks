import unittest

from main import (
    N_LESS_THAN_K_ERROR_MSG,
    NEGATIVE_VALUE_TEMPL,
    NOT_INT_VALUE_TEMPL,
    PATH_LENGTH_NOT_INT,
    PATH_LENGTH_NOT_POS,
    binomial_coefficient_iter,
    binomial_coefficient_rec,
    get_triangle_path_count,
)

BINOMIAL_FUNCTIONS = (binomial_coefficient_iter, binomial_coefficient_rec)


def _closed_path_count(length: int) -> int:
    return (2**length + 2 * ((-1) ** length)) // 3


class TestTrianglePath(unittest.TestCase):
    """Набор тестов подсчёта маршрутов"""

    def test_length_two(self):
        """Длина 2"""
        self.assertEqual(get_triangle_path_count(2), 2)

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(2.0)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)



    def test_known_lengths(self):
        for length in range(1, 11):
            with self.subTest(length=length):
                self.assertEqual(
                    get_triangle_path_count(length),
                    _closed_path_count(length),
                )

    def test_invalid_length_types(self):
        for value in ("3", None, True, False, 3.5):
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as error:
                    get_triangle_path_count(value)
                self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)

    def test_invalid_length_values(self):
        for value in (0, -1, -10):
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as error:
                    get_triangle_path_count(value)
                self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)


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

    def test_known_values(self):
        cases = (
            (0, 0, 1),
            (5, 0, 1),
            (5, 5, 1),
            (10, 3, 120),
            (30, 20, 30045015),
        )
        for func in BINOMIAL_FUNCTIONS:
            for n, k, expected in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), expected)

    def test_all_small_values(self):
        import math

        for func in BINOMIAL_FUNCTIONS:
            for n in range(16):
                for k in range(n + 1):
                    with self.subTest(func=func.__name__, n=n, k=k):
                        self.assertEqual(func(n, k), math.comb(n, k))

    def test_invalid_types(self):
        for func in BINOMIAL_FUNCTIONS:
            for value in ("a", 2.5, None, True, False):
                for param in ("n", "k"):
                    with self.subTest(func=func.__name__, value=value, param=param):
                        n, k = (value, 2) if param == "n" else (5, value)
                        with self.assertRaises(TypeError) as error:
                            func(n, k)
                        self.assertEqual(
                            str(error.exception),
                            NOT_INT_VALUE_TEMPL.format(param),
                        )

    def test_negative_values(self):
        for func in BINOMIAL_FUNCTIONS:
            for n, k, param in ((-1, 0, "n"), (5, -1, "k")):
                with self.subTest(func=func.__name__, param=param):
                    with self.assertRaises(ValueError) as error:
                        func(n, k)
                    self.assertEqual(
                        str(error.exception),
                        NEGATIVE_VALUE_TEMPL.format(param),
                    )

    def test_n_less_than_k_both(self):
        for func in BINOMIAL_FUNCTIONS:
            for n, k in ((0, 1), (1, 2), (5, 10)):
                with self.subTest(func=func.__name__, n=n, k=k):
                    with self.assertRaises(ValueError) as error:
                        func(n, k)
                    self.assertEqual(
                        str(error.exception),
                        N_LESS_THAN_K_ERROR_MSG,
                    )


if __name__ == "__main__":
    unittest.main()
