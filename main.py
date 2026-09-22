from functools import lru_cache

from profilehooks import profile


@profile
@lru_cache
def fibonacci_rec(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована рекурсивно согласно
    формуле вычисления последовательности.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


@profile
def fibonacci_iter(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно с использованием
    массива для хранения вычисляемых данных.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    numbers = [1, 1]
    for i in range(n - 2):
        numbers.append(numbers[-2] + numbers[-1])
    return numbers[-1]


@profile
def fibonacci(n: int) -> int:
    """Возвращает N-е число Фибоначчи. Реализована итеративно без использования массива.

    :param n: порядковый номер числа Фибоначчи
    :return: число Фибоначчи
    """
    cache = {"a": 1, "b": 1}

    k = len(cache)

    for i in range(n - k):
        a = cache["a"]
        b = cache["b"]
        cache["a"] = b
        cache["b"] = a + b
    return cache["b"]


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
