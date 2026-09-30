import unittest

from main import stars_and_bars


class TestStarsAndBars(unittest.TestCase):
    """Набор тестов для проверки функции генерации строк «звёзды
    и перегородки»"""

    def test_none(self):
        """Проверяет, что функция выбрасывает исключение при передаче None"""
        self.assertRaises(Exception, stars_and_bars, None, 2)
        self.assertRaises(Exception, stars_and_bars, 2, None)

    def test_invalid_n(self):
        """Проверяет, что функция выбрасывает исключение при n меньше 1"""
        for n in (0, -1):
            with self.subTest(n=n):
                self.assertRaises(Exception, stars_and_bars, n, 2)

    def test_negative_k(self):
        """Проверяет, что функция выбрасывает исключение при отрицательном k"""
        self.assertRaises(Exception, stars_and_bars, 3, -1)

    def test_one_box(self):
        """Проверяет единственную строку при одном ящике"""
        self.assertEqual(stars_and_bars(1, 3), ["***"])
        self.assertEqual(stars_and_bars(1, 0), [""])

    def test_zero_items(self):
        """Проверяет распределение нуля предметов: только перегородки"""
        self.assertEqual(stars_and_bars(3, 0), ["||"])

    def test_two_boxes_two_items(self):
        """Проверяет все строки для двух ящиков и двух предметов"""
        self.assertCountEqual(stars_and_bars(2, 2), ["**|", "*|*", "|**"])

    def test_three_boxes_one_item(self):
        """Проверяет все строки для трёх ящиков и одного предмета"""
        self.assertCountEqual(stars_and_bars(3, 1), ["*||", "|*|", "||*"])


if __name__ == "__main__":
    unittest.main()
