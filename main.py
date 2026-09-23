from functools import lru_cache

from profilehooks import profile


@profile
@lru_cache
def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно согласно
    формуле вычисления последовательности.

    :n <= 0: функция вернёт 0
    :n == 1: функция вернёт 1
    в остальных случаях будет применён алгоритм вычисления (см. код)

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n <= 0:
        return 0

    if n == 1:
        return 1

    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


@profile
def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно с использованием
    массива для хранения вычисляемых данных.

    при n <= 0 функция вернёт 0
    при n == 1 функция вернёт 1
    в остальных случаях будет применён алгоритм вычисления (см. код)

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n <= 0:
        return 0

    if n == 1:
        return 1

    numbers = [1, 1]
    for _ in range(n - 2):
        numbers.append(numbers[-2] + numbers[-1])

    return numbers[-1]


@profile
def fibonacci(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно без использования массива.

    при n <= 0 функция вернёт 0
    при n == 1 функция вернёт 1
    в остальных случаях будет применён алгоритм вычисления (см. код)

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n <= 0:
        return 0

    if n == 1:
        return 1

    a = 1
    b = 1

    for _ in range(n - 2):
        a, b = b, a + b

    return b


def main():
    n = 35
    print(f"Вычисление {n} числа Фибоначчи рекурсивно:")
    print(fibonacci_rec(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно:")
    print(fibonacci_iter(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно без использования массива:")
    print(fibonacci(n))


if __name__ == "__main__":
    main()
