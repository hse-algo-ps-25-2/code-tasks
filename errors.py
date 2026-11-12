from enum import StrEnum


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках приложения."""

    NOT_STR_NAME = "Название задачи не является строкой"
    EMPTY_NAME = "Название задачи является пустой строкой"
    NOT_NUMBER_DUR = "Продолжительность задачи не является числом"
    NEG_NUMBER_DUR = "Продолжительность задачи меньше или равна нулю"
    START_NOT_NUMBER = "Момент начала выполнения задачи не является числом"
    START_NEG_NUMBER = "Момент начала выполнения задачи меньше нуля"
    DUR_NOT_NUMBER = "Продолжительность выполнения задачи не является числом"
    DUR_NOT_POS_NUMBER = "Продолжительность выполнения задачи меньше или равна нулю"
    TASKS_NOT_LIST = "Некорректный формат списка задач для составления расписания"
    TASKS_EMPTY_LIST = "Список задач для составления расписания пуст"
    EXECUTOR_NOT_INT = "Индекс исполнителя не является целым неотрицательным числом"
    EXECUTOR_OUT_OF_RANGE = "Индекс исполнителя превышает количество исполнителей"


class ErrorTemplates(StrEnum):
    """Перечисление шаблонов сообщений об ошибках приложения."""

    INVALID_TASK = "Некорректный формат задачи на позиции [{0}] в списке задач для составления расписания"


class ScheduleError(Exception):
    """Общая ошибка расписания.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)


class ScheduleItemError(ScheduleError):
    """Ошибка некорректного параметра инициализации элемента расписания.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)


class ScheduleArgumentError(ScheduleError):
    """Ошибка некорректного параметра при инициализации расписания.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)


class TaskArgumentError(ScheduleError):
    """Ошибка некорректного параметра инициализации задачи.
    Attributes:
        message -- Сообщение об ошибке.
    """

    def __init__(self, message):
        super().__init__(message)
