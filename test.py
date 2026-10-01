import unittest

from main import (
    LENGTH_NOT_INT,
    LENGTH_NOT_POS,
    NOT_LIST,
    check_zero_one_strings,
    generate_strings_naive,
)


class TestNaiveGenerator(unittest.TestCase):
    """Набор тестов наивного генератора"""

    def test_length_two(self):
        """Длина 2"""
        self.assertCountEqual(generate_strings_naive(2), ["01", "10", "11"])

    def test_not_int_length(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings_naive(2.0)
        self.assertEqual(LENGTH_NOT_INT, str(error.exception))

    def test_validator_accepts_result(self):
        """Валидатор принимает набор наивного генератора"""
        strings = generate_strings_naive(3)
        self.assertTrue(check_zero_one_strings(3, strings))


class TestZeroOneValidator(unittest.TestCase):
    """Набор тестов валидатора"""

    def test_length_two(self):
        """Полный набор длины 2"""
        self.assertTrue(check_zero_one_strings(2, ["01", "10", "11"]))

    def test_lecture_example(self):
        """Пример длины 3 с лекции"""
        strings = ["010", "011", "110", "101", "111"]
        self.assertTrue(check_zero_one_strings(3, strings))

    def test_missing_string(self):
        """Неполный набор"""
        self.assertFalse(check_zero_one_strings(2, ["01", "11"]))

    def test_not_int_length(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            check_zero_one_strings(1.5, ["0", "1"])
        self.assertEqual(LENGTH_NOT_INT, str(error.exception))

    def test_negative_length(self):
        """Отрицательная длина"""
        with self.assertRaises(ValueError) as error:
            check_zero_one_strings(-1, [])
        self.assertEqual(LENGTH_NOT_POS, str(error.exception))


if __name__ == "__main__":
    unittest.main()
