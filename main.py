from collections import namedtuple

INF = float("inf")
TABLE_NOT_NUMBERS = "Таблица цен не является списком списков чисел"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"
TABLE_IS_EMPTY = "Таблица цен пустая"
INCORRECT_DATA_TYPE = "Некорректный тип данных"

Result = namedtuple("Result", ["cost", "path"])


def _validate(price_table: list[list[float | int]]) -> None:
    """Проводит валидацию таблицы.

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    """
    if not isinstance(price_table, list):
        raise TypeError(INCORRECT_DATA_TYPE)

    if len(price_table) == 0:
        raise ValueError(TABLE_IS_EMPTY)

    if len(price_table[0]) == 0:
        raise ValueError(TABLE_IS_EMPTY)

    width = None
    for row in price_table:
        if not isinstance(row, list):
            raise TypeError(INCORRECT_DATA_TYPE)
        if width is None:
            width = len(row)
        elif len(row) != width:
            raise ValueError(TABLE_NOT_RECT)
        for item in row:
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                raise TypeError(TABLE_NOT_NUMBERS)


def _table_inf_expand(price_table: list[list[float | int]]) -> list[list[float | int]]:
    """Дополняет таблицу бесконечностями.

    Изначальная первая строка становится второй
    — на её месте появляется строка с бесконечностями

    Изначальный первый столбец становится вторым
    — на его месте появляется столбец с бесконечностями

    :param price_table: прямоугольная таблица цен посещения ячеек
    :return new_price_table: таблица, дополненная слева и сверху бесконечностями
    """
    height = len(price_table)
    zero_row = [float("inf") for i in range(height + 1)]

    new_price_table = [zero_row]

    for row in price_table:
        new_price_table.append((row[::-1] + [float("inf")])[::-1])

    return new_price_table


def _table_inf_clear(price_table: list[list[float | int]]) -> list[list[float | int]]:
    """Функция, обратная **_table_enf_expand()**.

    Удаляет из таблицы нули, полученные путём дополнения

    :param price_table: прямоугольная таблица цен посещения ячеек,
    дополненная слева и сверху бесконечностями
    :return new_price_table: чистая таблица без бесконечностей
    """
    price_table = [x[1:] for x in price_table[1:]]
    return price_table


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    _validate(price_table)

    height, width = len(price_table), len(price_table[0])
    costs = [[0] * width for _ in range(height)]
    costs[0][0] = price_table[0][0]

    for j in range(1, width):
        costs[0][j] = costs[0][j - 1] + price_table[0][j]
    for i in range(1, height):
        costs[i][0] = costs[i - 1][0] + price_table[i][0]
    for i in range(1, height):
        for j in range(1, width):
            costs[i][j] = price_table[i][j] + min(costs[i - 1][j], costs[i][j - 1])

    path = [(height - 1, width - 1)]
    i, j = height - 1, width - 1
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        elif costs[i - 1][j] <= costs[i][j - 1]:
            i -= 1
        else:
            j -= 1
        path.append((i, j))
    path.reverse()

    return Result(cost=costs[-1][-1], path=path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
