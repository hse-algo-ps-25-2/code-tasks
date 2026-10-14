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

    def test_length_one(self):
        """Длина 1 — базовый случай"""
        result = generate_strings(1)
        self.assertEqual(sorted(result), ["0", "1"])

    def test_length_two(self):
        """Длина 2"""
        self.assertTrue(check_strings(generate_strings(2), 2))

    def test_length_three(self):
        """Длина 3"""
        self.assertTrue(check_strings(generate_strings(3), 3))

    def test_length_four(self):
        """Длина 4"""
        self.assertTrue(check_strings(generate_strings(4), 4))

    def test_length_five(self):
        """Длина 5"""
        self.assertTrue(check_strings(generate_strings(5), 5))

    def test_no_duplicates(self):
        """Все строки уникальны"""
        result = generate_strings(6)
        self.assertEqual(len(result), len(set(result)))

    def test_all_lengths_correct(self):
        """Все строки имеют нужную длину"""
        for length in range(1, 8):
            with self.subTest(length=length):
                for s in generate_strings(length):
                    self.assertEqual(len(s), length)

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_zero(self):
        """Длина 0"""
        with self.assertRaises(ValueError) as error:
            generate_strings(0)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_negative(self):
        """Длина отрицательное"""
        with self.assertRaises(ValueError) as error:
            generate_strings(-3)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_known_values_both(self):
        """Известные значения для обеих функций"""
        cases = [
            (1, 0, 1),
            (1, 1, 1),
            (2, 1, 2),
            (4, 2, 6),
            (5, 0, 1),
            (5, 5, 1),
            (6, 3, 20),
            (10, 5, 252),
        ]
        for func in BINOMIAL_FUNCTIONS:
            for n, k, expected in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), expected)

    def test_matches_between_functions(self):
        """Итеративная и рекурсивная дают одинаковый результат"""
        for n in range(0, 12):
            for k in range(n + 1):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        binomial_coefficient_iter(n, k),
                        binomial_coefficient_rec(n, k),
                    )

    def test_n_less_than_k(self):
        """n меньше k"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_iter(1, 2)
        self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_n_negative(self):
        """n отрицательное"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_iter(-1, 0)
        self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))

    def test_k_negative(self):
        """k отрицательное"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_iter(5, -1)
        self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))

    def test_n_is_not_int(self):
        """n не целое"""
        with self.assertRaises(TypeError) as error:
            binomial_coefficient_rec("a", 2)
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))

    def test_k_is_not_int(self):
        """k не целое"""
        with self.assertRaises(TypeError) as error:
            binomial_coefficient_iter(5, 2.5)
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))


class TestCheckStrings(unittest.TestCase):
    """Набор тестов функции check_strings"""

    def test_incorrect_with_00(self):
        """Набор содержит '00'"""
        self.assertFalse(check_strings(["01", "10", "00"], 2))

    def test_incomplete_set(self):
        """Набор неполный"""
        self.assertFalse(check_strings(["01", "10"], 2))

    def test_wrong_length(self):
        """Строка неправильной длины"""
        self.assertFalse(check_strings(["01", "10", "111"], 2))

    def test_duplicates(self):
        """Дубликаты"""
        self.assertFalse(check_strings(["01", "01", "10", "11"], 2))

    def test_invalid_characters(self):
        """Недопустимые символы"""
        self.assertFalse(check_strings(["01", "10", "12"], 2))

    def test_not_string(self):
        """Элемент — не строка"""
        self.assertFalse(check_strings(["01", 10, "11"], 2))

    def test_length_negative(self):
        """Отрицательная длина"""
        self.assertFalse(check_strings([], -1))

    def test_length_zero(self):
        """Длина 0"""
        self.assertTrue(check_strings([], 0))

    def test_correct_length_one(self):
        """Корректный набор длины 1"""
        self.assertTrue(check_strings(["0", "1"], 1))

    def test_correct_length_two(self):
        """Корректный набор длины 2"""
        self.assertTrue(check_strings(["01", "10", "11"], 2))

    def test_correct_length_three(self):
        """Корректный набор длины 3"""
        self.assertTrue(check_strings(["010", "011", "101", "110", "111"], 3))


if __name__ == "__main__":
    unittest.main()
