from collections import namedtuple

INF = float("inf")
TABLE_NOT_NUMBERS = "Таблица цен не является списком списков чисел"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def _validate_price_table(price_table: list[list[float | int]]) -> None:
    """Проверяет, что таблица непустая, прямоугольная и содержит числа."""
    if type(price_table) is not list:
        raise TypeError(TABLE_NOT_NUMBERS)

    if any(type(row) is not list for row in price_table):
        raise TypeError(TABLE_NOT_NUMBERS)

    if not price_table or not price_table[0]:
        raise ValueError(TABLE_NOT_RECT)

    width = len(price_table[0])
    if any(len(row) != width for row in price_table):
        raise ValueError(TABLE_NOT_RECT)

    for row in price_table:
        for value in row:
            if type(value) not in (int, float):
                raise TypeError(TABLE_NOT_NUMBERS)


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз.

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    _validate_price_table(price_table)

    height = len(price_table)
    width = len(price_table[0])

    costs = [[INF] * width for _ in range(height)]
    previous = [[None] * width for _ in range(height)]

    costs[0][0] = price_table[0][0]

    for column in range(1, width):
        costs[0][column] = costs[0][column - 1] + price_table[0][column]
        previous[0][column] = (0, column - 1)

    for row in range(1, height):
        costs[row][0] = costs[row - 1][0] + price_table[row][0]
        previous[row][0] = (row - 1, 0)

    for row in range(1, height):
        for column in range(1, width):
            from_top = costs[row - 1][column]
            from_left = costs[row][column - 1]

            if from_top < from_left:
                costs[row][column] = from_top + price_table[row][column]
                previous[row][column] = (row - 1, column)
            else:
                costs[row][column] = from_left + price_table[row][column]
                previous[row][column] = (row, column - 1)

    path = []
    current = (height - 1, width - 1)

    while current is not None:
        path.append(current)
        row, column = current
        current = previous[row][column]

    path.reverse()

    return Result(cost=costs[-1][-1], path=path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
