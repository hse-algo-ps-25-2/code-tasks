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


def _validate_list(profit_matrix: list[list[float | int]]):
    if (
        not isinstance(profit_matrix, list)
        or not all(isinstance(sublist, list) for sublist in profit_matrix)
        or not all(
            (isinstance(item_of_sublit, int) or isinstance(item_of_sublit, float))
            and not isinstance(item_of_sublit, bool)
            for sublist in profit_matrix
            for item_of_sublit in sublist
        )
    ):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    if (
        not len(profit_matrix)
        or not profit_matrix[0]
        or any(len(row) != len(profit_matrix[0]) for row in profit_matrix)
    ):
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    for project_idx in range(0, len(profit_matrix[0])):
        prev_profit = 0
        for lots_count in range(0, len(profit_matrix)):
            cur_profit = profit_matrix[lots_count][project_idx]

            if cur_profit < 0:
                raise ProfitValueError(
                    ErrorMessages.NEG_PROFIT, project_idx, lots_count
                )
            if cur_profit < prev_profit:
                raise ProfitValueError(
                    ErrorMessages.DECR_PROFIT, project_idx, lots_count
                )
            prev_profit = cur_profit


def _get_invest_distributions_rec(
    max_profits: list[list[float | int]],
    profit_matrix: list[list[float | int]],
    project_count: int,
    lot_count: int,
    current_distribution: list[int],
    distributions: list[list[int]],
) -> None:
    if project_count == 0:
        if lot_count == 0:
            distributions.append(current_distribution[::-1])
        return

    project_idx = project_count - 1

    for cur_project_lots in range(lot_count + 1):
        prev_project_lots = lot_count - cur_project_lots

        cur_profit = (
            0
            if cur_project_lots == 0
            else profit_matrix[cur_project_lots - 1][project_idx]
        )

        prev_profit = max_profits[prev_project_lots][project_idx]

        if prev_profit + cur_profit == max_profits[lot_count][project_count]:
            _get_invest_distributions_rec(
                max_profits,
                profit_matrix,
                project_count - 1,
                prev_project_lots,
                current_distribution + [cur_project_lots],
                distributions,
            )


def get_invest_distributions(
    profit_matrix: list[list[float | int]],
) -> Result:
    """Возвращает максимальную прибыль и все оптимальные распределения лотов."""
    _validate_list(profit_matrix)

    lot_count = len(profit_matrix)
    project_count = len(profit_matrix[0])

    max_profits = [[UNREACHABLE] * (project_count + 1) for _ in range(lot_count + 1)]
    max_profits[0][0] = 0

    for lots in range(1, lot_count + 1):
        max_profits[lots][0] = UNREACHABLE

    for project_idx in range(1, project_count + 1):
        max_profits[0][project_idx] = 0

    for project_idx in range(1, project_count + 1):
        for lots in range(1, lot_count + 1):
            best_profit = UNREACHABLE

            for cur_project_lots in range(lots + 1):
                prev_project_lots = lots - cur_project_lots

                cur_profit = (
                    0
                    if cur_project_lots == 0
                    else profit_matrix[cur_project_lots - 1][project_idx - 1]
                )

                prev_profit = max_profits[prev_project_lots][project_idx - 1]

                if prev_profit != UNREACHABLE:
                    candidate_profit = prev_profit + cur_profit

                    if candidate_profit > best_profit:
                        best_profit = candidate_profit

            max_profits[lots][project_idx] = best_profit

    distributions: list[list[int]] = []

    _get_invest_distributions_rec(
        max_profits,
        profit_matrix,
        project_count,
        lot_count,
        [],
        distributions,
    )

    return Result(max_profits[lot_count][project_count], distributions)


def main():
    profit_matrix = [[1, 1, 1], [2, 3, 2], [2, 2, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == "__main__":
    main()
