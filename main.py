from collections import namedtuple
from enum import StrEnum

UNREACHABLE = float("-inf")


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""

    TABLE_NOT_NUMBERS = "Таблица прибыли не является списком списков чисел"
    TABLE_NOT_RECT = "Таблица прибыли не является прямоугольной матрицей"
    NEG_PROFIT = "Значение прибыли не может быть отрицательно"
    DECR_PROFIT = "Значение прибыли не может убывать с ростом инвестиций"


Result = namedtuple("Result", ["profit", "distribution"])


class ProfitValueError(Exception):
    def __init__(self, message: str, project_idx: int, row_idx: int) -> None:
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def _is_number(value: object) -> bool:
    """Число ли это: bool числом не считается."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_shape(profit_matrix: object) -> None:
    """Проверяет, что аргумент — непустая прямоугольная таблица (список списков).

    :raise TypeError: если аргумент не список списков
    :raise ValueError: если таблица пустая или непрямоугольная
    """
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    for row in profit_matrix:
        if not isinstance(row, list):
            raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    width = len(profit_matrix[0])
    for row in profit_matrix:
        if len(row) != width:
            raise ValueError(ErrorMessages.TABLE_NOT_RECT)


def _check_numbers(profit_matrix: list[list]) -> None:
    """Проверяет, что в клетках таблицы только числа.

    :raise TypeError: если найдено нечисло (bool числом не считается)
    """
    for row in profit_matrix:
        for value in row:
            if not _is_number(value):
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)


def _check_profits(profit_matrix: list[list[float | int]]) -> None:
    """Проверяет прибыль: она неотрицательна и не убывает по столбцу.

    :raise ProfitValueError: если прибыль отрицательна или убывает с ростом вложения
    """
    for row_idx, row in enumerate(profit_matrix):
        for project_idx, value in enumerate(row):
            if value < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)

    width = len(profit_matrix[0])
    for row_idx in range(1, len(profit_matrix)):
        for project_idx in range(width):
            prev = profit_matrix[row_idx - 1][project_idx]
            if profit_matrix[row_idx][project_idx] < prev:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, project_idx, row_idx)


def _validate(profit_matrix: object) -> list[list[float | int]]:
    """Проверяет форму таблицы и значения в ней.

    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательна или убывает по столбцу
    """
    _check_shape(profit_matrix)
    _check_numbers(profit_matrix)
    _check_profits(profit_matrix)
    return profit_matrix


def _project_profit(
    profit_matrix: list[list[float | int]], project: int, lots: int
) -> float | int:
    """Прибыль проекта, если ему дали lots лотов (ноль лотов — прибыль 0)."""
    if lots == 0:
        return 0
    return profit_matrix[lots - 1][project]


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    matrix = _validate(profit_matrix)
    lots_total = len(matrix)
    projects = len(matrix[0])

    best = [[UNREACHABLE] * (lots_total + 1) for _ in range(projects + 1)]
    choice = [[0] * (lots_total + 1) for _ in range(projects + 1)]
    best[0][0] = 0

    for i in range(1, projects + 1):
        for j in range(lots_total + 1):
            for lots in range(j + 1):
                prev = best[i - 1][j - lots]
                if prev == UNREACHABLE:
                    continue
                candidate = prev + _project_profit(matrix, i - 1, lots)
                if best[i][j] == UNREACHABLE or candidate > best[i][j]:
                    best[i][j] = candidate
                    choice[i][j] = lots

    distribution = [0] * projects
    left = lots_total
    for i in range(projects, 0, -1):
        lots = choice[i][left]
        distribution[i - 1] = lots
        left -= lots

    return Result(profit=best[projects][lots_total], distribution=distribution)


def main():
    profit_matrix = [
        [15, 18, 16, 17],
        [20, 22, 23, 19],
        [26, 28, 27, 25],
        [34, 33, 29, 31],
        [40, 39, 41, 37],
    ]
    print(get_invest_distribution(profit_matrix))


if __name__ == "__main__":
    main()
