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


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам.
    План восстанавливается после расчёта прибыли

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    _validate_table(profit_matrix)
    levels = len(profit_matrix)
    projects = len(profit_matrix[0])
    profits = [[UNREACHABLE] * (levels + 1) for _ in range(projects + 1)]
    profits[0][0] = 0

    for project in range(1, projects + 1):
        for lots in range(levels + 1):
            for invested in range(lots + 1):
                previous = profits[project - 1][lots - invested]
                if previous == UNREACHABLE:
                    continue
                gain = profit_matrix[invested - 1][project - 1] if invested else 0
                profits[project][lots] = max(profits[project][lots], previous + gain)

    distribution = _restore_distribution(profit_matrix, profits)
    return Result(profits[projects][levels], distribution)


def _validate_table(matrix: list[list[float | int]]) -> None:
    if not isinstance(matrix, list) or any(not isinstance(row, list) for row in matrix):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)
    if any(
        not isinstance(value, (int, float)) or isinstance(value, bool)
        for row in matrix
        for value in row
    ):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    _validate_profits(matrix)


def _validate_profits(matrix: list[list[float | int]]) -> None:
    for row_idx, row in enumerate(matrix):
        for project_idx, value in enumerate(row):
            if value < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)
            if row_idx > 0 and value < matrix[row_idx - 1][project_idx]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, project_idx, row_idx)


def _restore_distribution(matrix, profits) -> list[int]:
    remaining = len(matrix)
    projects = len(matrix[0])
    distribution = [0] * projects
    for project in range(projects, 0, -1):
        for invested in range(remaining + 1):
            previous = profits[project - 1][remaining - invested]
            if previous == UNREACHABLE:
                continue
            gain = matrix[invested - 1][project - 1] if invested else 0
            if previous + gain == profits[project][remaining]:
                distribution[project - 1] = invested
                remaining -= invested
                break
    return distribution


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
