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

    def test_length_three(self):
        """Длина 3"""
        self.assertEqual(get_triangle_path_count(3), 2)

    def test_length_four(self):
        """Длина 4"""
        self.assertEqual(get_triangle_path_count(4), 6)

    def test_length_five(self):
        """Длина 5"""
        self.assertEqual(get_triangle_path_count(5), 4 * 2 + 2)

    def test_length_six(self):
        """Длина 6"""
        self.assertEqual(get_triangle_path_count(6), 2 + 4 * 3 + 8)

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(2.0)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)

    def test_length_non_positive(self):
        """Длина не положительная"""
        with self.assertRaises(ValueError) as error:
            get_triangle_path_count(0)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)

        with self.assertRaises(ValueError) as negError:
            get_triangle_path_count(-1)
        self.assertEqual(str(negError.exception), PATH_LENGTH_NOT_POS)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_full_4_both(self):
        """C(4, k) для всех k у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            result4 = [1, 4, 6, 4, 1]
            n = 4
            with self.subTest(func=func.__name__):
                for k in range(n + 1):
                    self.assertEqual(func(n, k), result4[k])

    def test_full_5_both(self):
        """C(5, k) для всех k у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            result5 = [1, 5, 10, 10, 5, 1]
            n = 5
            with self.subTest(func=func.__name__):
                for k in range(n + 1):
                    self.assertEqual(func(n, k), result5[k])

    def test_big_both(self):
        """C(30, 20) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(30, 20), 30045015)

    def test_result_int(self):
        """Результат - целое у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(type(func(30, 20)), int)

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
            binomial_coefficient_rec(2, "k")
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_n_is_not_pos(self):
        """n не положительное"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_rec(-3, 1)
        self.assertIn(
            str(error.exception),
            [NEGATIVE_VALUE_TEMPL.format("n"), N_LESS_THAN_K_ERROR_MSG],
        )

    def test_k_is_not_pos(self):
        """k не положительное"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_rec(2, -10)
        self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))


if __name__ == "__main__":
    unittest.main()
