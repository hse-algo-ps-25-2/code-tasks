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

    height = len(price_table)

    if height == 0:
        raise ValueError(TABLE_IS_EMPTY)

    for row in price_table:
        length = len(row)
        if height != length:
            raise ValueError(TABLE_NOT_RECT)

        for item in row:
            if not (isinstance(item, int) or isinstance(item, float)):
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


def _table_fill_costs(price_table: list[list[float | int]]) -> list[list[float | int]]:
    price_table = _table_inf_expand(price_table)
    new_price_table = price_table

    for row in range(len(price_table) - 1):
        for column in range(len(price_table) - 1):
            current_cell = price_table[row + 1][column + 1]
            up_cell = price_table[row][column + 1]
            left_cell = price_table[row + 1][column]
            best_previous_way = min(up_cell, left_cell)

            if best_previous_way == float("inf"):
                best_previous_way = 0

            new_price_table[row + 1][column + 1] = current_cell + best_previous_way

    return new_price_table


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    _validate(price_table)
    price_table = _table_inf_clear(_table_fill_costs(price_table))
    return price_table


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
