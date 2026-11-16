from abstract_schedule import AbstractSchedule
from schedule_item import ScheduleItem
from task import Task


class Schedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач и количества
    исполнителей. Для построения расписания используется Ленточная стратегия.

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

    def __init__(self, tasks: list[Task], executor_count: int):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :param executor_count: Количество исполнителей.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате.
        """
        super().__init__(tasks, executor_count)

        # Рассчитывается и сохраняется в приватном поле класса минимальная
        # продолжительность расписания
        self._duration = self.__calculate_duration()

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule_for_each_executor()

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._duration

    def __calculate_duration(self) -> float:
        """Вычисляет и возвращает минимальную продолжительность расписания"""
        total_duration = sum(task.duration for task in self._tasks)
        max_task_duration = max(task.duration for task in self._tasks)
        return float(max(max_task_duration, total_duration / self.executor_count))

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        t_opt = self._duration

        task_idx = 0
        task_offset = 0.0

        for executor_idx in range(self.executor_count):
            cursor = 0.0

            while cursor < t_opt and task_idx < self.task_count:
                task = self._tasks[task_idx]
                remaining = task.duration - task_offset
                piece = min(remaining, t_opt - cursor)

                if piece > 0:
                    self._executor_schedule[executor_idx].append(
                        ScheduleItem(task, cursor, piece)
                    )
                    cursor += piece
                    task_offset += piece

                if task_offset >= task.duration:
                    task_idx += 1
                    task_offset = 0.0

            if cursor < t_opt:
                self._executor_schedule[executor_idx].append(
                    ScheduleItem(None, cursor, t_opt - cursor)
                )
