from queue import Queue

PUBERTY_TIME = 2

def validate_param(value):
    if not isinstance(value, int):
        raise TypeError('Значение должно быть числом')


def validate_month(value):
    validate_param(value)
    if value < 1:
         raise ValueError('Значение должно быть больше либо равно единице')

def validate_lifetime(value):
    validate_param(value)
    if value < 2:
         raise ValueError('Значение должно быть больше либо равно единице')

def rabbit_life_req(couple, que, cur_month, lifetime):
    count = 1

    if cur_month >= couple + PUBERTY_TIME:
        children_count = cur_month - (couple + PUBERTY_TIME)
        for _ in range(children_count):
            que.enqueue(cur_month)
            count += rabbit_life_req(cur_month, que, cur_month, lifetime)



    if cur_month == couple + lifetime:
        que.dequeue()
        count -= 1
        new_oldest_couple = que.peek()
        count += rabbit_life_req(new_oldest_couple, que, cur_month, lifetime)

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

    que = Queue()
    que.enqueue(1)
    count = 1
    
    for cur_month in range(2, month):
        couple = que.peek()
        count += rabbit_life_req(couple, que, cur_month, lifetime)
     
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
