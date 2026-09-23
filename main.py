import time


def gcd_recursive(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Рекурсивная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    n, k = abs(a), abs(b)

    if n == 0 or k == 0:
        return n or k

    if n > k:
        n, k = k, n

    return gcd_recursive(k - n, n)


def gcd_iterative_slow(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Медленная итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    n, k = abs(a), abs(b)

    if n > k:
        n, k = k, n

    while n != 0 and k != 0:
        n, k = k - n, n
        if n > k:
            n, k = k, n

    return n or k


def gcd_iterative_fast(a: int, b: int) -> int:
    """Вычисляет наибольший общий делитель двух целых чисел.
    Быстрая итеративная реализация

    :param a: целое число a
    :param b: целое число b
    :return: значение наибольшего общего делителя
    """
    n, k = abs(a), abs(b)

    if n > k:
        n, k = k, n

    while n != 0 and k != 0:
        n, k = k % n, n

    return n or k


def lcm(a: int, b: int) -> int:
    """Вычисляет наименьшее общее кратное двух натуральных чисел

    :param a: натуральное число a
    :param b: натуральное число b
    :return: значение наименьшего общего кратного
    """
    n, k = abs(a), abs(b)
    return (n * k) // gcd_iterative_fast(n, k)


def main():
    a = 1005002
    b = 1354
    print(f"Вычисление НОД чисел {a} и {b} рекурсивно:")
    start_time = time.time()
    print(gcd_recursive(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с вычитанием:")
    start_time = time.time()
    print(gcd_iterative_slow(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОД чисел {a} и {b} итеративно с делением:")
    start_time = time.time()
    print(gcd_iterative_fast(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")

    print(f"\nВычисление НОК чисел {a} и {b}:")
    start_time = time.time()
    print(lcm(a, b))
    print(f"Продолжительность: {time.time() - start_time} сек")


if __name__ == "__main__":
    main()
