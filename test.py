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

    def test_length_one(self):
        """Длина 1"""
        self.assertEqual(get_triangle_path_count(1), 0)

    def test_length_two(self):
        """Длина 2"""
        self.assertEqual(get_triangle_path_count(2), 2)

    def test_length_paths(self):
        """
        Проверка соответствие вычисленного значения формуле
        """
        for i in range(3, 101):
            with self.subTest(length=i):
                self.assertEqual(get_triangle_path_count(i), _closed_path_count(i))

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(2.0)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(True)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(False)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)

    def test_length_less_than_one(self):
        """Длина меньше 1"""
        with self.assertRaises(ValueError) as error:
            get_triangle_path_count(0)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)
        with self.assertRaises(ValueError) as error:
            get_triangle_path_count(-1)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_big_both(self):
        """C(20, 10) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(20, 10), 184756)

    def test_k_zero(self):
        """C(n, 0) = 1"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 0), 1)

    def test_k_equals_n(self):
        """C(n, n) = 1"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 5), 1)

    def test_zero_zero(self):
        """C(0, 0) = 1"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(0, 0), 1)

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

    def test_k_is_not_int(self):
        """k не целое"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(2, "b")
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_n_is_bool(self):
        """n типа bool"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(True, 0)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))

    def test_k_is_bool(self):
        """k типа bool"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(5, False)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_n_negative(self):
        """n отрицательное"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(-1, 0)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))

    def test_k_negative(self):
        """k отрицательное"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(1, -1)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))


if __name__ == "__main__":
    unittest.main()
