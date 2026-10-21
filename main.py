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


def _validate_profit_matrix(profit_matrix: list[list[float | int]]) -> None:
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    if not all(isinstance(row, list) for row in profit_matrix):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    projects = len(profit_matrix[0])
    if any(len(row) != projects for row in profit_matrix):
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)
    if any(
        isinstance(value, bool) or not isinstance(value, (int, float))
        for row in profit_matrix
        for value in row
    ):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    _validate_profit_values(profit_matrix)


def _validate_profit_values(profit_matrix: list[list[float | int]]) -> None:
    for row_idx, row in enumerate(profit_matrix):
        for project_idx, value in enumerate(row):
            if value < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)
            if row_idx > 0 and value < profit_matrix[row_idx - 1][project_idx]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, project_idx, row_idx)


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    _validate_profit_matrix(profit_matrix)
    lots = len(profit_matrix)
    projects = len(profit_matrix[0])
    max_profit = [[UNREACHABLE] * (lots + 1) for _ in range(projects + 1)]
    chosen_lots = [[0] * (lots + 1) for _ in range(projects + 1)]
    max_profit[0][0] = 0

    # Строка i учитывает первые i проектов, столбец j — ровно j лотов.
    for project in range(1, projects + 1):
        for total_lots in range(lots + 1):
            for current_lots in range(total_lots + 1):
                previous_profit = max_profit[project - 1][total_lots - current_lots]
                if previous_profit == UNREACHABLE:
                    continue
                current_profit = 0
                if current_lots > 0:
                    current_profit = profit_matrix[current_lots - 1][project - 1]
                candidate = previous_profit + current_profit
                if candidate > max_profit[project][total_lots]:
                    max_profit[project][total_lots] = candidate
                    chosen_lots[project][total_lots] = current_lots

    distribution = [0] * projects
    remaining_lots = lots
    for project in range(projects, 0, -1):
        current_lots = chosen_lots[project][remaining_lots]
        distribution[project - 1] = current_lots
        remaining_lots -= current_lots

    return Result(max_profit[projects][lots], distribution)


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
