import unittest

from main import (
    ErrorMessages,
    binomial_coefficient_iter,
    binomial_coefficient_rec,
    generate_strings,
)
from strings_checker import check_strings

BINOMIAL_COEFFICIENT_FUNCTIONS = (binomial_coefficient_iter, binomial_coefficient_rec)


class TestZeroOneStringsChecker(unittest.TestCase):
    """Набор тестов валидатора генератора строк из 0 и 1 без 00"""

    def test_length_two(self):
        """Полный набор длины 2"""
        self.assertTrue(check_strings(["01", "10", "11"], 2))

    def test_length_3(self):
        """Полный набор длины 3"""
        strings = ["010", "011", "110", "111", "101"]
        self.assertTrue(check_strings(strings, 3))

    def test_missing_string(self):
        """Неполный набор"""
        self.assertFalse(check_strings(["01", "11"], 2))

    def test_not_str_in_string(self):
        """Не Строка в strings"""
        self.assertFalse(check_strings(["01", "11", 10], 2))

    def test_duplicate(self):
        """Повтор строки"""
        self.assertFalse(check_strings(["01", "01", "11"], 2))

    def test_wrong_length(self):
        """Строка другой длины"""
        self.assertFalse(check_strings(["01", "10", "111"], 2))

    def test_bad_chars(self):
        """Символы помимо 0 и 1"""
        self.assertFalse(check_strings(["01", "10", "12"], 2))

    def test_not_str_element(self):
        """Не только строка на входе"""
        self.assertFalse(check_strings(["01", "10", 11], 2))

    def test_two_zeros_in_row(self):
        """В строке два нуля подряд"""
        self.assertFalse(check_strings(["00", "10", "11"], 2))

    def test_extra_string(self):
        """Лишняя строка"""
        self.assertFalse(check_strings(["01", "10", "11", "00"], 2))


class TestZeroOneStringGenerator(unittest.TestCase):
    """Набор тестов генератора строк из 0 и 1 без 00"""

    def test_validator_accepts_result_length_two(self):
        """Валидатор принимает набор наивного генератора длины 2"""
        self.assertTrue(check_strings(generate_strings(2), 2))

    def test_length_not_int(self):
        """Правильный TypeError если длина не целое число"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), ErrorMessages.LENGTH_NOT_INT)

    def test_negative_length(self):
        """Правильный ValueError если длина отрицательная"""
        with self.assertRaises(ValueError) as error:
            generate_strings(-1)
        self.assertEqual(ErrorMessages.LENGTH_NOT_POS, str(error.exception))

    def test_zero_length(self):
        """Правильный ValueError если длина нулевая"""
        with self.assertRaises(ValueError) as error:
            generate_strings(0)
        self.assertEqual(ErrorMessages.LENGTH_NOT_POS, str(error.exception))

    def test_validator_accepts_result_length_3(self):
        """Валидатор принимает набор наивного генератора длины 3"""
        strings = generate_strings(3)
        self.assertTrue(check_strings(strings, 3))

    def test_validator_accepts_result_length_10(self):
        """Валидатор принимает набор наивного генератора длины 10"""
        strings = generate_strings(10)
        self.assertTrue(check_strings(strings, 10))


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов вычисления биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) == 10 у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_n_less_than_k_both(self):
        """Правильный ValueError если n меньше k у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(1, 2)
                self.assertEqual(
                    str(error.exception), ErrorMessages.N_LESS_THAN_K_ERROR_MSG
                )

    def test_n_is_not_int_both(self):
        """Правильный TypeError если n не целое число у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func("a", 2)
                self.assertEqual(
                    str(error.exception), ErrorMessages.NOT_INT_VALUE_TEMPL.format("n")
                )

    def test_k_is_not_int_both(self):
        """Правильный TypeError если k не целое число у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    binomial_coefficient_rec(5, "2")
                self.assertEqual(
                    str(error.exception), ErrorMessages.NOT_INT_VALUE_TEMPL.format("k")
                )

    def test_all_comb_4_k_both(self):
        """C(4, k) для всех k у обеих функций\
            соотвествует элементу номер k строки 4 треугольника Паскаля"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            pascal_triangle_string_4 = [1, 4, 6, 4, 1]
            n = 4
            with self.subTest(func=func.__name__):
                for k in range(n + 1):
                    self.assertEqual(func(n, k), pascal_triangle_string_4[k])

    def test_all_comb_5_k_both(self):
        """C(5, k) для всех k у обеих функций\
            соотвествует элементу номер k строки 5 треугольника Паскаля"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            pascal_triangle_string_5 = [1, 5, 10, 10, 5, 1]
            n = 5
            with self.subTest(func=func.__name__):
                for k in range(n + 1):
                    self.assertEqual(func(n, k), pascal_triangle_string_5[k])

    def test_all_comb_6_k_both(self):
        """C(6, k) для всех k у обеих функций\
            соотвествует элементу номер k строки 6 треугольника Паскаля"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            pascal_triangle_string_6 = [1, 6, 15, 20, 15, 6, 1]
            n = 6
            with self.subTest(func=func.__name__):
                for k in range(n + 1):
                    self.assertEqual(func(n, k), pascal_triangle_string_6[k])

    def test_big_both(self):
        """C(30, 20) == 30045015 у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(30, 20), 30045015)

    def test_result_is_int_both(self):
        """Результат - целое число у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(type(func(3, 2)), int)

    def test_n_is_negative_both(self):
        """Правильный ValueError если n отрицательное у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(-3, -7)
                self.assertEqual(
                    str(error.exception), ErrorMessages.NEGATIVE_VALUE_TEMPL.format("n")
                )

    def test_k_is_not_pos_both(self):
        """Правильный ValueError если k отрицательное у обеих функций"""
        for func in BINOMIAL_COEFFICIENT_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(2, -10)
                self.assertEqual(
                    str(error.exception), ErrorMessages.NEGATIVE_VALUE_TEMPL.format("k")
                )


if __name__ == "__main__":
    unittest.main()
