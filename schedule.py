from fractions import Fraction

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
        durations = [Fraction(str(task.duration)) for task in self.tasks]
        max_task_duration = max(durations)
        total_duration = sum(durations)
        average_duration = total_duration / self.executor_count

        self._exact_duration = max(max_task_duration, average_duration)
        return float(self._exact_duration)

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        executor_idx = 0
        current_time = Fraction(0)
        duration = self._exact_duration

        for task in self.tasks:
            remaining_duration = Fraction(str(task.duration))

            while remaining_duration > 0:
                available_time = duration - current_time

                if available_time == 0:
                    executor_idx += 1
                    current_time = Fraction(0)
                    available_time = duration

                execution_duration = min(remaining_duration, available_time)

                self._executor_schedule[executor_idx].append(
                    ScheduleItem(
                        task,
                        float(current_time),
                        float(execution_duration),
                    )
                )

                remaining_duration -= execution_duration
                current_time += execution_duration

        for idx, executor_schedule in enumerate(self._executor_schedule):
            if idx < executor_idx:
                continue

            last_end = current_time if idx == executor_idx else Fraction(0)
            downtime_duration = duration - last_end

            if downtime_duration > 0:
                executor_schedule.append(
                    ScheduleItem(
                        None,
                        float(last_end),
                        float(downtime_duration),
                    )
                )
