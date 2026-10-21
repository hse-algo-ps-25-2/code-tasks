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
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_structure(profit_matrix: list) -> None:
    if not profit_matrix:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)
    for row in profit_matrix:
        if not isinstance(row, list):
            raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    first_row_length = len(profit_matrix[0])
    if first_row_length == 0 or any(
        len(row) != first_row_length for row in profit_matrix
    ):
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)


def _check_numbers(profit_matrix: list) -> None:
    for row in profit_matrix:
        for value in row:
            if not _is_number(value):
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)


def _check_non_negative(profit_matrix: list) -> None:
    for row_idx, row in enumerate(profit_matrix):
        for project_idx, value in enumerate(row):
            if value < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)


def _check_non_decreasing(profit_matrix: list) -> None:
    for row_idx in range(1, len(profit_matrix)):
        for project_idx in range(len(profit_matrix[0])):
            previous = profit_matrix[row_idx - 1][project_idx]
            current = profit_matrix[row_idx][project_idx]
            if current < previous:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, project_idx, row_idx)


def _validate_profit_matrix(profit_matrix: object) -> None:
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    _check_structure(profit_matrix)
    _check_numbers(profit_matrix)
    _check_non_negative(profit_matrix)
    _check_non_decreasing(profit_matrix)


def _profit_of(project_idx: int, lots: int, profit_matrix: list) -> float | int:
    if lots == 0:
        return 0
    return profit_matrix[lots - 1][project_idx]


def _build_max_profits(profit_matrix: list) -> list:
    lots_count = len(profit_matrix)
    projects_count = len(profit_matrix[0])
    max_profits: list[list[float | int]] = [
        [0] * (lots_count + 1) for _ in range(projects_count + 1)
    ]
    for project_idx in range(1, projects_count + 1):
        for lots in range(1, lots_count + 1):
            best = UNREACHABLE
            for current_project_lots in range(lots + 1):
                previous_project_lots = lots - current_project_lots
                candidate = max_profits[project_idx - 1][
                    previous_project_lots
                ] + _profit_of(project_idx - 1, current_project_lots, profit_matrix)
                if candidate > best:
                    best = candidate
            max_profits[project_idx][lots] = best
    return max_profits


def _restore_distribution(profit_matrix: list, max_profits: list) -> list:
    lots_count = len(profit_matrix)
    projects_count = len(profit_matrix[0])
    distribution = [0] * projects_count
    remaining_lots = lots_count
    for project_idx in range(projects_count, 0, -1):
        if project_idx == 1:
            lot_options = (remaining_lots,)
        else:
            lot_options = range(remaining_lots + 1)
        for current_project_lots in lot_options:
            previous_project_lots = remaining_lots - current_project_lots
            candidate = max_profits[project_idx - 1][
                previous_project_lots
            ] + _profit_of(project_idx - 1, current_project_lots, profit_matrix)
            if candidate == max_profits[project_idx][remaining_lots]:
                distribution[project_idx - 1] = current_project_lots
                remaining_lots = previous_project_lots
                break
        else:
            raise RuntimeError("Оптимальный план не найден обратным ходом")
    return distribution


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам.
    План восстанавливается после расчёта прибыли

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    _validate_profit_matrix(profit_matrix)
    max_profits = _build_max_profits(profit_matrix)
    distribution = _restore_distribution(profit_matrix, max_profits)
    total_profit = max_profits[len(profit_matrix[0])][len(profit_matrix)]
    return Result(total_profit, distribution)


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
