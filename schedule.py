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
        """Вычисляет и возвращает минимальную продолжительность расписания."""
        total_duration = sum(task.duration for task in self.tasks)
        maximum_task_duration = max(task.duration for task in self.tasks)

        # float нужен, чтобы продолжительность всегда была вещественной
        # (max может вернуть целое число, если оно встретилось первым)
        return float(max(maximum_task_duration, total_duration / self.executor_count))

    def __fill_schedule_for_each_executor(self) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, на основе исходного списка задач и общей продолжительности
        расписания."""
        tasks = self.tasks
        task_index = 0
        remaining_task_duration = tasks[0].duration
        # Допуск для сравнения дробных чисел
        epsilon = 1e-9

        for executor_index in range(self.executor_count):
            local_position = 0.0

            # Заполняем окно исполнителя кусками ленты
            while self._duration - local_position > epsilon and task_index < len(tasks):
                piece_duration = min(
                    remaining_task_duration, self._duration - local_position
                )

                if piece_duration > 0:
                    current_task = tasks[task_index]
                    self._executor_schedule[executor_index].append(
                        ScheduleItem(current_task, local_position, piece_duration)
                    )
                    local_position += piece_duration
                    remaining_task_duration -= piece_duration

                # Задача закончилась, переходим к следующей
                if remaining_task_duration <= epsilon:
                    task_index += 1
                    if task_index < len(tasks):
                        remaining_task_duration = tasks[task_index].duration

            # Оставшуюся часть окна заполняем простоем
            if self._duration - local_position > epsilon:
                self._executor_schedule[executor_index].append(
                    ScheduleItem(None, local_position, self._duration - local_position)
                )
