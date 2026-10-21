from collections import namedtuple

INF = float("inf")
TABLE_NOT_LISTS = "Таблица цен не является списком списков"
CELL_NOT_NUMBER = "Клетка таблицы не является числом или None"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def _validate_price_table(
    price_table: list[list[float | int | None]],
) -> None:
    """Проверяет тип, форму и содержимое таблицы цен.

    :param price_table: таблица стоимостей клеток
    :raise TypeError: если таблица не список списков или содержит
        значения, отличные от int, float и None
    :raise ValueError: если таблица пустая или непрямоугольная
    """
    if not isinstance(price_table, list):
        raise TypeError(TABLE_NOT_LISTS)

    if not all(isinstance(row, list) for row in price_table):
        raise TypeError(TABLE_NOT_LISTS)

    if not price_table or not price_table[0]:
        raise ValueError(TABLE_NOT_RECT)

    width = len(price_table[0])

    if any(len(row) != width for row in price_table):
        raise ValueError(TABLE_NOT_RECT)

    for row in price_table:
        for cell in row:
            if cell is not None and type(cell) not in (int, float):
                raise TypeError(CELL_NOT_NUMBER)


def _build_cost_table(
    price_table: list[list[float | int | None]],
) -> list[list[float]]:
    """Строит таблицу минимальных стоимостей достижения клеток.

    :param price_table: проверенная прямоугольная таблица цен
    :return: таблица накопленных минимальных стоимостей
    """
    height = len(price_table)
    width = len(price_table[0])

    cost_table = [[INF] * width for _ in range(height)]

    if price_table[0][0] is None:
        return cost_table

    cost_table[0][0] = price_table[0][0]

    for row in range(height):
        for column in range(width):
            if row == 0 and column == 0:
                continue

            cell_cost = price_table[row][column]

            if cell_cost is None:
                continue

            cost_from_top = cost_table[row - 1][column] if row > 0 else INF
            cost_from_left = cost_table[row][column - 1] if column > 0 else INF

            previous_cost = min(cost_from_top, cost_from_left)

            if previous_cost != INF:
                cost_table[row][column] = previous_cost + cell_cost

    return cost_table


def _restore_path(
    cost_table: list[list[float]],
) -> list[tuple[int, int]]:
    """Восстанавливает оптимальный путь от финиша к старту.

    :param cost_table: таблица минимальных стоимостей
    :return: список координат от старта до финиша
    """
    row = len(cost_table) - 1
    column = len(cost_table[0]) - 1

    path = [(row, column)]

    while row > 0 or column > 0:
        if row == 0:
            column -= 1
        elif column == 0:
            row -= 1
        elif cost_table[row - 1][column] <= cost_table[row][column - 1]:
            row -= 1
        else:
            column -= 1

        path.append((row, column))

    path.reverse()
    return path


def get_min_cost_path(price_table: list[list[float | int | None]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз. None в клетке
    запрещает посещение. Если пути нет, cost и path равны None

    :param price_table: прямоугольная таблица цен, None — запрещённая клетка
    :raise TypeError: если аргумент не список списков либо клетка не число
        и не None
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и путём либо Result(None, None)
    """
    _validate_price_table(price_table)

    if price_table[0][0] is None or price_table[-1][-1] is None:
        return Result(None, None)

    cost_table = _build_cost_table(price_table)
    min_cost = cost_table[-1][-1]

    if min_cost == INF:
        return Result(None, None)

    path = _restore_path(cost_table)
    return Result(cost=min_cost, path=path)


def main():
    table = [[1.1, None], [3, 4]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
