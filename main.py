from collections import namedtuple

INF = float("inf")
TABLE_NOT_LISTS = "Таблица цен не является списком списков"
CELL_NOT_NUMBER = "Клетка таблицы не является числом или None"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def _validate_table(price_table: list[list[float | int | None]]) -> tuple[int, int]:
    """Проверяет структуру таблицы и типы значений, возвращает (rows, cols)."""
    if type(price_table) is not list:
        raise TypeError(TABLE_NOT_LISTS)

    rows = len(price_table)
    if rows == 0:
        raise ValueError(TABLE_NOT_RECT)

    cols = None
    for row in price_table:
        if type(row) is not list:
            raise TypeError(TABLE_NOT_LISTS)

        row_len = len(row)
        if row_len == 0:
            raise ValueError(TABLE_NOT_RECT)

        if cols is None:
            cols = row_len
        elif row_len != cols:
            raise ValueError(TABLE_NOT_RECT)

        for cell in row:
            if type(cell) is bool or (
                cell is not None and (type(cell) not in (int, float))
            ):
                raise TypeError(CELL_NOT_NUMBER)

    return rows, cols


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
    rows, cols = _validate_table(price_table)

    if price_table[0][0] is None or price_table[rows - 1][cols - 1] is None:
        return Result(None, None)

    dp = [[INF] * cols for i in range(rows)]
    dp[0][0] = price_table[0][0]

    for r in range(rows):
        for c in range(cols):
            if (r, c) == (0, 0) or price_table[r][c] is None:
                continue

            prev_min = INF
            if r > 0 and dp[r - 1][c] < prev_min:
                prev_min = dp[r - 1][c]
            if c > 0 and dp[r][c - 1] < prev_min:
                prev_min = dp[r][c - 1]

            if prev_min != INF:
                dp[r][c] = prev_min + price_table[r][c]

    if dp[rows - 1][cols - 1] == INF:
        return Result(None, None)

    path = []
    r, c = rows - 1, cols - 1

    while (r, c) != (0, 0):
        path.append((r, c))
        from_top = dp[r - 1][c] if r > 0 else INF
        from_left = dp[r][c - 1] if c > 0 else INF

        if from_top <= from_left:
            r -= 1
        else:
            c -= 1

    path.append((0, 0))
    path.reverse()

    return Result(cost=dp[rows - 1][cols - 1], path=path)


def main() -> None:
    table = [[1.1, None], [3, 4]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
