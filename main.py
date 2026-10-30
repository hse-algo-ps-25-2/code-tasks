from queue import Queue

PUBERTY_TIME = 2


def validate_param(value):
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("Значение должно быть числом")


def validate_month(value):
    validate_param(value)
    if value < 1:
        raise ValueError("Значение должно быть больше либо равно единице")


def validate_lifetime(value):
    validate_param(value)
    if value < 2:
        raise ValueError("Значение должно быть больше либо равно двойке")


def rabbit_life_req(couple_birth, que, lifetime, finalMonth):
    count = 1
    death_month = couple_birth + lifetime
    first_parenting_month = couple_birth + PUBERTY_TIME
    for month in range(first_parenting_month, finalMonth):
        que.enqueue(month)
        count += rabbit_life_req(month, que, lifetime, finalMonth)

        if death_month == month:
            count -= 1
            que.dequeue()
            break
    return count


def rabbits(month: int, lifetime: int) -> int:
    """Возвращает количество живых пар кроликов в месяце month.

    В месяце 1 жива одна пара, родившаяся в этом месяце. Пара, родившаяся
    в месяце t, не приносит потомства в месяцах t и t + 1. С месяца t + 2
    она каждый месяц приносит одну новую пару, в том числе в месяц смерти.
    Пара живёт lifetime месяцев и входит в численность месяцев
    t, ..., t + lifetime - 1. В месяце t + lifetime она умирает и в число
    живых пар этого месяца не входит.

    :param month: номер месяца, целое число не меньше 1
    :param lifetime: продолжительность жизни в месяцах, целое число не меньше 2
    :raises TypeError: аргумент не целое число; bool не допускается
    :raises ValueError: month < 1 или lifetime < 2
    :return: число живых пар
    """
    validate_month(month)
    validate_lifetime(lifetime)
    count = 0
    que = Queue()
    que.enqueue(0)
    first_couple_birth = que.peek()
    count += rabbit_life_req(first_couple_birth, que, lifetime, month)

    return count


def main():
    queue = Queue()
    for value in (1, 2, 2):
        queue.enqueue(value)
    print("Начало очереди:", queue.peek())
    print("Вышло:", queue.dequeue())
    print("Пар на 8-й месяц при жизни 7 месяцев:", rabbits(8, 7))


if __name__ == "__main__":
    main()
