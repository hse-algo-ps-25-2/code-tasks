from math import isclose

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
        total_duration = sum(task.duration for task in self.tasks)
        max_duration = max(task.duration for task in self.tasks)
        average_duration = total_duration / self.executor_count
        
        return float(max(max_duration, average_duration))

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        executor_idx = 0
        current_time = 0.0

        for task in self.tasks:
            remaining_duration = task.duration

            while remaining_duration > 0:
                available_duration = self.duration - current_time
                fragment_duration = min(remaining_duration, available_duration)

                self._executor_schedule[executor_idx].append(
                    ScheduleItem(task, current_time, fragment_duration)
                )

                remaining_duration -= fragment_duration
                current_time += fragment_duration

                if isclose(remaining_duration, 0.0, abs_tol=1e-12):
                    remaining_duration = 0.0

                if isclose(current_time, self.duration, abs_tol=1e-12):
                    executor_idx += 1
                    current_time = 0.0

        if executor_idx < self.executor_count and current_time > 0:
            downtime_duration = self.duration - current_time
            if downtime_duration > 0:
                self._executor_schedule[executor_idx].append(
                    ScheduleItem(None, current_time, downtime_duration)
                )
            executor_idx += 1

        while executor_idx < self.executor_count:
            self._executor_schedule[executor_idx].append(
                ScheduleItem(None, 0.0, self.duration)
            )
            executor_idx += 1
