import unittest

from main import ErrorMessages, Result, coin_change


def _assert_valid_change(test_case, coins, amount, result, expected_count):
    test_case.assertEqual(result.count, expected_count)
    test_case.assertEqual(len(result.combination), expected_count)
    test_case.assertEqual(sum(result.combination), amount)
    allowed = set(coins)
    for coin in result.combination:
        test_case.assertIn(coin, allowed)


class TestCoinChange(unittest.TestCase):
    """Набор тестов размена монет"""

    def test_none_coins(self):
        """coins равен None"""
        with self.assertRaises(TypeError) as error:
            coin_change(None, 10)
        self.assertEqual(str(error.exception), ErrorMessages.COINS_NOT_LIST)

    def test_empty_coins(self):
        """Пустой список номиналов"""
        with self.assertRaises(ValueError) as error:
            coin_change([], 10)
        self.assertEqual(str(error.exception), ErrorMessages.WRONG_COINS)

    def test_none_amount(self):
        """amount равен None"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, 2, 5], None)
        self.assertEqual(str(error.exception), ErrorMessages.AMOUNT_NOT_INT)

    def test_coin_not_int(self):
        """Номинал не целое"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, 2.5, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.COIN_NOT_INT)

    def test_negative_amount(self):
        """Отрицательная сумма"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, 2, 5], -5)
        self.assertEqual(str(error.exception), ErrorMessages.WRONG_AMOUNT)

    def test_negative_coin(self):
        """Отрицательный номинал"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, -2, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.NEGATIVE_COIN)

    def test_zero_coin(self):
        """Нулевой номинал"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, 0, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.NEGATIVE_COIN)

    def test_impossible(self):
        """Сумму набрать нельзя"""
        self.assertEqual(coin_change([3, 7], 5), Result(None, None))

    def test_zero_amount(self):
        """Сумма 0"""
        self.assertEqual(coin_change([1, 2, 5], 0), Result(0, []))

    def test_single_coin(self):
        """Одна монета совпадает с суммой"""
        self.assertEqual(coin_change([1, 3, 7, 10], 7), Result(1, [7]))

    def test_basic(self):
        """Пример: 13 из 1, 2 и 5"""
        coins = [1, 2, 5]
        result = coin_change(coins, 13)
        _assert_valid_change(self, coins, 13, result, 4)

    def test_two_optima(self):
        """Несколько наборов из двух монет"""
        coins = [1, 3, 4]
        result = coin_change(coins, 6)
        _assert_valid_change(self, coins, 6, result, 2)

    def test_one_denomination(self):
        """Один номинал"""
        self.assertEqual(coin_change([2], 8), Result(4, [2, 2, 2, 2]))

    def assert_change(self, coins, amount, expected_count):
        """Проверяет корректность минимального набора монет"""
        result = coin_change(coins, amount)

        self.assertIsInstance(result, Result)
        self.assertEqual(result.count, expected_count)
        self.assertEqual(len(result.combination), expected_count)
        self.assertEqual(sum(result.combination), amount)

        for coin in result.combination:
            self.assertIn(coin, coins)

    def assert_error(self, exception, message, coins, amount):
        """Проверяет тип исключения и сообщение об ошибке"""
        with self.assertRaises(exception) as context:
            coin_change(coins, amount)

        self.assertEqual(str(context.exception), message)

    def test_greedy_failure(self):
        """Проверка случая, когда жадный алгоритм не оптимален"""
        self.assert_change([1, 7, 10], 14, 2)

    def test_unsorted_coins(self):
        """Номиналы монет заданы в произвольном порядке"""
        self.assert_change([4, 1, 3], 6, 2)

    def test_duplicate_coins(self):
        """Список содержит повторяющиеся номиналы"""
        self.assert_change([1, 3, 3], 6, 2)

    def test_without_one(self):
        """Размен суммы без номинала 1"""
        self.assert_change([4, 6], 8, 2)

    def test_unreachable_odd(self):
        """Нечётную сумму нельзя набрать чётными номиналами"""
        self.assertEqual(
            coin_change([4, 6], 7),
            Result(None, None),
        )

    def test_coins_larger_than_amount(self):
        """Все номиналы больше заданной суммы"""
        self.assertEqual(
            coin_change([5, 9], 3),
            Result(None, None),
        )

    def test_multiple_optimal(self):
        """Существует несколько различных оптимальных наборов"""
        self.assert_change([1, 2, 3], 4, 2)

    def test_tuple_coins(self):
        """coins является кортежем вместо списка"""
        self.assert_error(
            TypeError,
            ErrorMessages.COINS_NOT_LIST,
            (1, 2, 5),
            10,
        )

    def test_bool_amount(self):
        """amount является логическим значением"""
        self.assert_error(
            TypeError,
            ErrorMessages.AMOUNT_NOT_INT,
            [1, 2],
            True,
        )

    def test_float_amount(self):
        """amount является дробным числом"""
        self.assert_error(
            TypeError,
            ErrorMessages.AMOUNT_NOT_INT,
            [1, 2],
            5.5,
        )

    def test_bool_coin(self):
        """Номинал монеты является логическим значением"""
        self.assert_error(
            TypeError,
            ErrorMessages.COIN_NOT_INT,
            [1, True, 5],
            10,
        )

    def test_string_coin(self):
        """Номинал монеты является строкой"""
        self.assert_error(
            TypeError,
            ErrorMessages.COIN_NOT_INT,
            [1, "2", 5],
            10,
        )

    def test_invalid_coins_zero_amount(self):
        """Нулевой номинал при нулевой сумме"""
        self.assert_error(
            ValueError,
            ErrorMessages.NEGATIVE_COIN,
            [0, 1],
            0,
        )

    def test_empty_coins_zero_amount(self):
        """Пустой список номиналов при нулевой сумме"""
        self.assert_error(
            ValueError,
            ErrorMessages.WRONG_COINS,
            [],
            0,
        )

    def test_false_amount(self):
        """amount является логическим False"""
        self.assert_error(
            TypeError,
            ErrorMessages.AMOUNT_NOT_INT,
            [1, 2],
            False,
        )

    def test_false_coin(self):
        """Номинал монеты является логическим False"""
        self.assert_error(
            TypeError,
            ErrorMessages.COIN_NOT_INT,
            [1, False, 5],
            10,
        )

    def test_integral_float_amount(self):
        """amount является дробным типом с целым значением"""
        self.assert_error(
            TypeError,
            ErrorMessages.AMOUNT_NOT_INT,
            [1, 2],
            6.0,
        )

    def test_integral_float_coin(self):
        """Номинал имеет тип float с целым значением"""
        self.assert_error(
            TypeError,
            ErrorMessages.COIN_NOT_INT,
            [1, 2.0, 5],
            10,
        )

    def test_unreachable_single(self):
        """Сумму нельзя набрать единственным номиналом"""
        self.assertEqual(
            coin_change([4], 10),
            Result(None, None),
        )

    def test_unreachable_coprime(self):
        """Сумму нельзя набрать взаимно простыми номиналами"""
        self.assertEqual(
            coin_change([4, 7], 9),
            Result(None, None),
        )

    def test_large_amount(self):
        """Размен относительно большой суммы"""
        self.assert_change([1, 10, 100], 1000, 10)

    def test_result_type_impossible(self):
        """Невозможный размен возвращает именно Result"""
        result = coin_change([4, 7], 9)

        self.assertIs(type(result), Result)
        self.assertIsNone(result.count)
        self.assertIsNone(result.combination)

    def test_result_type_zero(self):
        """Нулевая сумма возвращает Result со списком монет"""
        result = coin_change([2], 0)

        self.assertIs(type(result), Result)
        self.assertEqual(result.count, 0)
        self.assertIs(type(result.combination), list)
        self.assertEqual(result.combination, [])


if __name__ == "__main__":
    unittest.main()
