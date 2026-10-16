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


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    _validate(price_table)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
