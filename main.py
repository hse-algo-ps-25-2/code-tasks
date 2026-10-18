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
            (isinstance(item_of_sublit, int) or isinstance(item_of_sublit, float)) and not isinstance(item_of_sublit, bool)
            for sublist in profit_matrix
            for item_of_sublit in sublist
        )
    ):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)


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
    _validate_list(profit_matrix)


def main():
    profit_matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == "__main__":
    main()
