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

    def test_negative_length(self):
        """Отрицательная длина"""
        with self.assertRaises(ValueError) as error:
            generate_strings_naive(-1)
        self.assertEqual(LENGTH_NOT_POS, str(error.exception))

    def test_zero_length(self):
        """Нулевая длина"""
        with self.assertRaises(ValueError) as error:
            generate_strings_naive(0)
        self.assertEqual(LENGTH_NOT_POS, str(error.exception))

    def test_validator_rejects_broken_result(self):
        """Валидатор не аппрувает подложный результат генератора"""
        strings = generate_strings_naive(3)
        strings.append("00")
        self.assertFalse(check_zero_one_strings(3, strings))

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

    def test_not_list(self):
        """Набор не список"""
        with self.assertRaises(TypeError) as error:
            check_zero_one_strings(2, ("01", "10", "11"))
        self.assertEqual(NOT_LIST, str(error.exception))

    def test_not_list_string(self):
        """Строка вместо списка"""
        with self.assertRaises(TypeError) as error:
            check_zero_one_strings(2, "011011")
        self.assertEqual(NOT_LIST, str(error.exception))

    def test_zero_length(self):
        """Нулевая длина"""
        with self.assertRaises(ValueError) as error:
            check_zero_one_strings(0, [])
        self.assertEqual(LENGTH_NOT_POS, str(error.exception))

    def test_duplicate(self):
        """Повтор строки"""
        self.assertFalse(
            check_zero_one_strings(2, ["01", "01", "10", "11"])
        )

    def test_wrong_length(self):
        """Строка другой длины"""
        self.assertFalse(
            check_zero_one_strings(2, ["01", "10", "111"])
        )

    def test_bad_chars(self):
        """Символы помимо 0 и 1"""
        self.assertFalse(
            check_zero_one_strings(2, ["01", "10", "12"])
        )

    def test_not_str_element(self):
        """Нет олько строка на входе"""
        self.assertFalse(
            check_zero_one_strings(2, ["01", "10", 11])
        )

    def test_two_zeros_in_row(self):
        """В строке два нуля подряд"""
        self.assertFalse(
            check_zero_one_strings(2, ["00", "01", "10", "11"])
        )

    def test_extra_string(self):
        """Лишняя строка"""
        self.assertFalse(
            check_zero_one_strings(2, ["01", "10", "11", "00"])
        )


if __name__ == "__main__":
    unittest.main()
