import unittest
from math import comb

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

    def test_length_one(self):
        """Длина 1 — минимальная"""
        self.assertTrue(check_strings(generate_strings(1), 1))
        self.assertEqual(sorted(generate_strings(1)), ["0", "1"])

    def test_length_three_exact(self):
        """Длина 3 — точный набор"""
        self.assertEqual(
            sorted(generate_strings(3)), ["010", "011", "101", "110", "111"]
        )

    def test_many_lengths(self):
        """Длины от 1 до 18 проходят чекер"""
        for length in range(1, 19):
            with self.subTest(length=length):
                self.assertTrue(check_strings(generate_strings(length), length))

    def test_returns_list_of_str(self):
        """Возвращается список строк"""
        result = generate_strings(4)
        self.assertIsInstance(result, list)
        for generated_string in result:
            self.assertIsInstance(generated_string, str)

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_wrong_types(self):
        """Длина: строка, None, список, bool"""
        for bad in ("2", None, [2], True, False, 1.5):
            with self.subTest(value=bad):
                with self.assertRaises(TypeError) as error:
                    generate_strings(bad)
                self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_not_positive(self):
        """Длина 0 и отрицательная"""
        for bad in (0, -1, -100):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError) as error:
                    generate_strings(bad)
                self.assertEqual(str(error.exception), LENGTH_NOT_POS)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_against_math_comb(self):
        """Сравнение с math.comb для n до 40"""
        for func in BINOMIAL_FUNCTIONS:
            for n in range(41):
                for k in range(n + 1):
                    with self.subTest(func=func.__name__, n=n, k=k):
                        self.assertEqual(func(n, k), comb(n, k))

    def test_edges(self):
        """Граничные случаи"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(0, 0), 1)
                self.assertEqual(func(7, 0), 1)
                self.assertEqual(func(7, 7), 1)
                self.assertEqual(func(7, 1), 7)
                self.assertEqual(func(30, 20), comb(30, 20))
                self.assertEqual(func(100, 50), comb(100, 50))

    def test_symmetry(self):
        """C(n, k) == C(n, n - k)"""
        for func in BINOMIAL_FUNCTIONS:
            for n in range(20):
                for k in range(n + 1):
                    self.assertEqual(func(n, k), func(n, n - k))

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
            for bad in ("a", 2.0, None, True, [5]):
                with self.subTest(func=func.__name__, n=bad):
                    with self.assertRaises(TypeError) as error:
                        func(bad, 2)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("n")
                    )

    def test_k_is_not_int(self):
        """k не целое"""
        for func in BINOMIAL_FUNCTIONS:
            for bad in ("a", 1.0, None, False, (1,)):
                with self.subTest(func=func.__name__, k=bad):
                    with self.assertRaises(TypeError) as error:
                        func(5, bad)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("k")
                    )

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
                    func(5, -1)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))

    def test_same_validation(self):
        """Обе функции проверяют вход одинаково"""
        cases = [
            ("a", 1),
            (1, "b"),
            (True, 1),
            (3, 1.5),
            (-1, 0),
            (3, -2),
            (2, 5),
            (-1, "x"),
        ]
        for n, k in cases:
            outcomes = []
            for func in BINOMIAL_FUNCTIONS:
                try:
                    func(n, k)
                    outcomes.append(None)
                except (TypeError, ValueError) as raised_error:
                    outcomes.append((type(raised_error), str(raised_error)))
            with self.subTest(n=n, k=k):
                self.assertEqual(outcomes[0], outcomes[1])


if __name__ == "__main__":
    unittest.main()
