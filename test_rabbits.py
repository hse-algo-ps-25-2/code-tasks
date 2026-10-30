import unittest

from main import rabbits


class TestRabbits(unittest.TestCase):
    """Публичные примеры задачи о кроликах."""

    def test_bool_arguments(self):
        """Булевы значения не принимаются как целые числа."""
        self.assertRaises(TypeError, rabbits, True, 7)
        self.assertRaises(TypeError, rabbits, False, 7)
        self.assertRaises(TypeError, rabbits, 7, True)
        self.assertRaises(TypeError, rabbits, 7, False)

    def test_invalid_types(self):
        """Проверка некорректных типов аргументов."""
        self.assertRaises(TypeError, rabbits, "5", 7)
        self.assertRaises(TypeError, rabbits, 5, "7")
        self.assertRaises(TypeError, rabbits, 5.0, 7)
        self.assertRaises(TypeError, rabbits, 5, 7.0)
        self.assertRaises(TypeError, rabbits, None, 7)
        self.assertRaises(TypeError, rabbits, 5, None)

    def test_invalid_values(self):
        """Невалидные данные приводят к исключениям."""
        self.assertRaises(ValueError, rabbits, 0, 2)
        self.assertRaises(ValueError, rabbits, -1, 2)
        self.assertRaises(ValueError, rabbits, 1, 1)
        self.assertRaises(ValueError, rabbits, 2, 0)

    def test_first_months(self):
        """До первой смерти численность совпадает с числами Фибоначчи."""
        self.assertEqual(rabbits(1, 2), 1)
        self.assertEqual(rabbits(2, 2), 1)
        self.assertEqual(rabbits(6, 8), 8)

    def test_first_death(self):
        """На 8-й месяц при жизни 7 месяцев остаётся 20 пар."""
        self.assertEqual(rabbits(8, 7), 20)

    def test_later_months(self):
        """Численность считается и после нескольких смертей."""
        self.assertEqual(rabbits(20, 7), 5266)
        self.assertEqual(rabbits(25, 7), 53515)

    def test_minimum_values(self):
        """Минимальные допустимые значения аргументов."""
        self.assertEqual(rabbits(1, 2), 1)
        self.assertEqual(rabbits(2, 2), 1)

    def test_death_month(self):
        """Пара размножается в месяц смерти, но не учитывается в популяции."""
        self.assertEqual(rabbits(3, 2), 1)
        self.assertEqual(rabbits(4, 2), 1)
        self.assertEqual(rabbits(8, 7), 20)

    def test_lifetime_boundary(self):
        """Проверка влияния продолжительности жизни на результат."""
        self.assertEqual(rabbits(8, 7), 20)
        self.assertEqual(rabbits(8, 8), 21)
        self.assertEqual(rabbits(8, 9), 21)

    def test_short_lifetime(self):
        """Проверка многократной смены поколений при короткой жизни."""
        self.assertEqual(rabbits(10, 2), 1)
        self.assertEqual(rabbits(20, 2), 1)

    def test_larger_lifetime(self):
        """Проверка роста популяции до первой смерти."""
        self.assertEqual(rabbits(10, 10), 55)
        self.assertEqual(rabbits(15, 20), 610)


if __name__ == "__main__":
    unittest.main()
