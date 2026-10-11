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


if __name__ == "__main__":
    unittest.main()
