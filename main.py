from collections import namedtuple
from enum import StrEnum

UNREACHABLE = float("-inf")


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""

    TABLE_NOT_NUMBERS = "Таблица прибыли не является списком списков чисел"
    TABLE_NOT_RECT = "Таблица прибыли не является прямоугольной матрицей"
    NEG_PROFIT = "Значение прибыли не может быть отрицательно"
    DECR_PROFIT = "Значение прибыли не может убывать с ростом инвестиций"


Result = namedtuple("Result", ["profit", "distributions"])


class ProfitValueError(Exception):
    def __init__(self, message: str, project_idx: int, row_idx: int) -> None:
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def validate_profit_matrix_shape(profit_matrix: list[list[float | int]]) -> None:
    """Выполняет проверку формы матрицы"""
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    if not all(isinstance(row, list) for row in profit_matrix):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    row_len = len(profit_matrix[0])
    for i in profit_matrix:
        if len(i) != row_len:
            raise ValueError(ErrorMessages.TABLE_NOT_RECT)


def validate_profit_matrix(
    profit_matrix: list[list[float | int]],
):
    """Выполняет проверку матрицы"""
    validate_profit_matrix_shape(profit_matrix)

    for i in profit_matrix:
        for j in i:
            if type(j) is not int and type(j) is not float:
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    for row_idx in range(len(profit_matrix)):
        for project_idx in range(len(profit_matrix[row_idx])):
            value = profit_matrix[row_idx][project_idx]
            if value < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)

    for row in range(len(profit_matrix) - 1):
        for col in range(len(profit_matrix[row])):
            if profit_matrix[row + 1][col] < profit_matrix[row][col]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, col, row + 1)


def collect_distributions(
    optimal_choices: list[list[list[int]]],
    lots_remaining: int,
    projects_remaining: int,
    current_distribution: list[int],
    distributions: list[list[int]],
):
    """Обходит сохраненные оптимальные распределения лотов
    и добавляет готовые планы в список результатов
    """
    if projects_remaining == 0:
        if lots_remaining == 0:
            distributions.append(current_distribution.copy())
        return

    project_id = projects_remaining - 1
    choices = optimal_choices[lots_remaining][projects_remaining]
    for lots_for_project in choices:
        current_distribution[project_id] = lots_for_project
        collect_distributions(
            optimal_choices,
            lots_remaining - lots_for_project,
            projects_remaining - 1,
            current_distribution,
            distributions,
        )


def build_distributions_set(
    optimal_choices: list[list[list[int]]], total_lots: int, total_projects: int
) -> list[list[int]]:
    """Собирает итоговые распределения инвестиций
    из сохраненных распределений лотов
    """
    distributions = []
    current_distribution = [0] * total_projects
    collect_distributions(
        optimal_choices, total_lots, total_projects, current_distribution, distributions
    )
    return distributions


def get_invest_distributions(
    profit_matrix: list[list[float | int]],
) -> Result:
    """Возвращает максимальную прибыль и все распределения всех лотов

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distributions
    """
    validate_profit_matrix(profit_matrix)

    total_lots = len(profit_matrix)
    total_projects = len(profit_matrix[0])
    max_profits = [[UNREACHABLE] * (total_projects + 1) for _ in range(total_lots + 1)]
    optimal_choices = [
        [[] for _ in range(total_projects + 1)] for _ in range(total_lots + 1)
    ]
    max_profits[0][0] = 0
    for project_num in range(1, total_projects + 1):
        project_id = project_num - 1

        for lots_for_step in range(total_lots + 1):
            for lots_for_project in range(lots_for_step + 1):
                lots_remaining = lots_for_step - lots_for_project
                previous_profit = max_profits[lots_remaining][project_num - 1]

                if previous_profit == UNREACHABLE:
                    continue

                project_profit = (
                    0
                    if lots_for_project == 0
                    else profit_matrix[lots_for_project - 1][project_id]
                )
                project_total_profit = previous_profit + project_profit

                if project_total_profit > max_profits[lots_for_step][project_num]:
                    max_profits[lots_for_step][project_num] = project_total_profit
                    optimal_choices[lots_for_step][project_num] = [lots_for_project]
                elif project_total_profit == max_profits[lots_for_step][project_num]:
                    optimal_choices[lots_for_step][project_num].append(lots_for_project)

    distributions = build_distributions_set(optimal_choices, total_lots, total_projects)
    return Result(
        profit=max_profits[total_lots][total_projects], distributions=distributions
    )


def main():
    profit_matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == "__main__":
    main()
