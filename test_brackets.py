import unittest

from main import is_brackets_balanced


class TestBrackets(unittest.TestCase):
    """Публичные примеры проверки скобок."""

    def test_empty_string(self):
        self.assertTrue(is_brackets_balanced(""))

    def test_no_brackets(self):
        self.assertTrue(is_brackets_balanced("A*B*C*D*E + HJFLSSF ;\\HJFRHP"))

    def test_single_pairs(self):
        self.assertTrue(is_brackets_balanced("()"))
        self.assertTrue(is_brackets_balanced("[]"))
        self.assertTrue(is_brackets_balanced("{}"))

    def test_non_depth(self):
        self.assertTrue(is_brackets_balanced("()[]{}"))

    def test_nested_pairs(self):
        self.assertTrue(is_brackets_balanced("(({[]})([])()){([!])}"))

    def test_extra_opening(self):
        self.assertFalse(is_brackets_balanced("((("))

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            is_brackets_balanced([])
            is_brackets_balanced(123)
            is_brackets_balanced(3.14)
            is_brackets_balanced({})
            is_brackets_balanced(b"()")

    def test_balanced_expression(self):
        """Скобки в арифметическом выражении согласованы."""
        self.assertTrue(is_brackets_balanced("3 + 2 * (5 - [4 / {2 + 1}])"))

    def test_extra_closing(self):
        """Лишняя закрывающая скобка."""
        self.assertFalse(is_brackets_balanced("(]"))

    def test_closing_without_opening(self):
        """Закрывающая скобка при пустом стеке."""
        self.assertFalse(is_brackets_balanced(")"))
        self.assertFalse(is_brackets_balanced("]"))
        self.assertFalse(is_brackets_balanced("}"))
        self.assertFalse(is_brackets_balanced("())"))


if __name__ == "__main__":
    unittest.main()
