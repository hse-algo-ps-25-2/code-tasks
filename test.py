import unittest
from  math import comb

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

    def test_any_result(self):
        """Проверяет, что количество строк соответсвует ожидаемому, отсутсвие
        дубликатов, строки состоят только из n-1 перегородок и k звездочек,
        что в совокупности гарантирует правильность результата"""
        cases = [(1, 0), (1, 5), (2, 2), (3, 1), (4, 3), (5, 5), (2, 7)]

        for n, k in cases:
            with self.subTest(n=n, k=k):
                result = stars_and_bars(n, k)

                expected_count = comb(n + k - 1, k)
                self.assertEqual(
                    len(result), expected_count,
                    f"n={n}, k={k}: ожидалось {expected_count} строк"
                )

                self.assertEqual(
                    len(set(result)), len(result),
                    f"n={n}, k={k}: в результате есть дубликаты"
                )

                for s in result:
                    self.assertEqual(
                        s.count("*"), k,
                        f"n={n}, k={k}: в {s!r} не {k} звёзд"
                    )
                    self.assertEqual(
                        s.count("|"), n - 1,
                        f"n={n}, k={k}: в {s!r} не {n-1} перегородок"
                    )
                    self.assertEqual(
                        len(s), n - 1 + k,
                        f"n={n}, k={k}: длина {s!r} не равна {n-1+k}"
                    )


if __name__ == "__main__":
    unittest.main()
