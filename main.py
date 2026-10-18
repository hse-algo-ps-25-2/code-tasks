from collections import namedtuple
from enum import StrEnum

INF = float("inf")


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""

    COINS_NOT_LIST = "coins должен быть списком"
    AMOUNT_NOT_INT = "amount должен быть целым числом"
    WRONG_COINS = "coins должен быть непустым списком положительных целых чисел"
    WRONG_AMOUNT = "amount должен быть неотрицательным целым числом"
    NEGATIVE_COIN = "монеты не могут быть отрицательными или нулевыми"
    COIN_NOT_INT = "все монеты должны быть целыми числами"


Result = namedtuple("Result", ["count", "combination"])


def _validate_coins(coins: list[int]) -> None:
    """Проверяет корректность списка номиналов

    :param coins: список положительных целых номиналов
    :raise TypeError: если coins не список или номинал не целое число
    :raise ValueError: если список пуст или номинал не больше 0
    :return: None, если список номиналов корректен
    """
    if not isinstance(coins, list):
        raise TypeError(ErrorMessages.COINS_NOT_LIST)

    if not coins:
        raise ValueError(ErrorMessages.WRONG_COINS)

    for coin in coins:
        if not isinstance(coin, int) or isinstance(coin, bool):
            raise TypeError(ErrorMessages.COIN_NOT_INT)

        if coin <= 0:
            raise ValueError(ErrorMessages.NEGATIVE_COIN)


def _validate_amount(amount: int) -> None:
    """Проверяет корректность заданной суммы

    :param amount: неотрицательная сумма
    :raise TypeError: если amount не целое число
    :raise ValueError: если сумма отрицательная
    :return: None, если сумма корректна
    """
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise TypeError(ErrorMessages.AMOUNT_NOT_INT)

    if amount < 0:
        raise ValueError(ErrorMessages.WRONG_AMOUNT)


def coin_change(coins: list[int], amount: int) -> Result:
    """Возвращает минимальное число монет и один такой набор номиналов

    :param coins: список положительных целых номиналов
    :param amount: неотрицательная сумма
    :raise TypeError: если coins не список либо amount или номинал не целое
    :raise ValueError: если список пуст, сумма отрицательная или номинал не больше 0
    :return: Result с полями count и combination либо Result(None, None)
    """
    _validate_coins(coins)
    _validate_amount(amount)

    min_coin_counts = [0] + [INF] * amount
    last_coin = [None] * (amount + 1)

    for current_sum in range(1, amount + 1):
        for coin in coins:
            if coin > current_sum:
                continue

            candidate = min_coin_counts[current_sum - coin] + 1

            if candidate < min_coin_counts[current_sum]:
                min_coin_counts[current_sum] = candidate
                last_coin[current_sum] = coin

    if min_coin_counts[amount] == INF:
        return Result(None, None)

    combination = []
    remaining = amount

    while remaining > 0:
        coin = last_coin[remaining]
        combination.append(coin)
        remaining -= coin

    return Result(min_coin_counts[amount], combination)


def main():
    coins = [1, 2, 5]
    amount = 13
    print(coin_change(coins, amount))


if __name__ == "__main__":
    main()
