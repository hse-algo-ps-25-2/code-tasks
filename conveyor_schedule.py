from abstract_schedule import AbstractSchedule
from errors import (
    ScheduleArgumentError,
    ErrorMessages,
    ErrorTemplates,
)
from schedule_item import ScheduleItem
from staged_task import StagedTask


class ConveyorSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач, состоящих
     из двух этапов и двух исполнителей. Для построения расписания используется
     алгоритм Джонсона.

    Properties
    ----------
    tasks(self) -> tuple[Task]:
        Возвращает исходный список задач для составления расписания.

    task_count(self) -> int:
        Возвращает количество задач для составления расписания.

    executor_count(self) -> int:
        Возвращает количество исполнителей.

    duration(self) -> float:
        Возвращает общую продолжительность расписания.

    Methods
    -------
    get_schedule_for_executor(self, executor_idx: int) -> tuple[ScheduleRow]:
        Возвращает расписание для указанного исполнителя.
    """

    def __init__(self, tasks: list[StagedTask]):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество этапов для какой-либо задачи не
        равно двум.
        """
        ConveyorSchedule.__validate_params(tasks)
        super().__init__(tasks, 2)

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""
        first_row = self._executor_schedule[0]
        second_row = self._executor_schedule[1]

        first_end = 0
        second_end = 0

        for task in tasks:
            stage1 = task.stage_duration(0)
            stage2 = task.stage_duration(1)

            first_row.append(ScheduleItem(task, first_end, stage1))
            first_end += stage1

  
            start = max(first_end, second_end)
            if start > second_end:
                second_row.append(ScheduleItem(None, second_end, start - second_end))
            second_row.append(ScheduleItem(task, start, stage2))
            second_end = start + stage2

 
        if second_end > first_end:
            first_row.append(ScheduleItem(None, first_end, second_end - first_end))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""

        first_group = [
            task for task in tasks if task.stage_duration(0) <= task.stage_duration(1)
        ]
        second_group = [
            task for task in tasks if task.stage_duration(0) > task.stage_duration(1)
        ]

        first_group = sorted(first_group, key=lambda task: task.stage_duration(0))
        second_group = sorted(
            second_group, key=lambda task: task.stage_duration(1), reverse=True
        )
        return first_group + second_group

    @staticmethod
    def __validate_params(tasks: list[StagedTask]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса ConveyorSchedule."""
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ErrorMessages.TASKS_EMPTY_LIST)
        for idx, value in enumerate(tasks):
            if not isinstance(value, StagedTask):
                raise ScheduleArgumentError(ErrorTemplates.INVALID_TASK.format(idx))
            if value.stage_count != 2:
                raise ScheduleArgumentError(
                    ErrorTemplates.INVALID_STAGE_CNT.format(idx)
                )
