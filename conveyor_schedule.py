from abstract_schedule import AbstractSchedule
from errors import (
    ErrorMessages,
    ErrorTemplates,
    ScheduleArgumentError,
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
        first_executor = self._executor_schedule[0]
        second_executor = self._executor_schedule[1]
        for task in tasks:
            first_duration = task.stage_duration(0)
            second_duration = task.stage_duration(1)

            first_start = first_executor[-1].end if first_executor else 0
            first_executor.append(ScheduleItem(task, first_start, first_duration))

            second_free = second_executor[-1].end if second_executor else 0
            second_start = max(first_executor[-1].end, second_free)
            if second_start > second_free:
                second_executor.append(
                    ScheduleItem(None, second_free, second_start - second_free)
                )
            second_executor.append(ScheduleItem(task, second_start, second_duration))

        # Второй исполнитель может закончить позже первого, тогда в конец
        # расписания первого добавляется простой до этого момента, чтобы
        # продолжительность расписания совпадала с моментом окончания
        # последнего интервала первого исполнителя.
        first_end = first_executor[-1].end
        second_end = second_executor[-1].end
        if second_end > first_end:
            first_executor.append(ScheduleItem(None, first_end, second_end - first_end))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        # Задания с a_i <= b_i идут первыми по возрастанию a_i,
        # остальные — по убыванию b_i.
        first_group = []
        second_group = []
        for task in tasks:
            if task.stage_duration(0) <= task.stage_duration(1):
                first_group.append(task)
            else:
                second_group.append(task)
        first_group.sort(key=lambda task: task.stage_duration(0))
        second_group.sort(key=lambda task: task.stage_duration(1), reverse=True)
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
