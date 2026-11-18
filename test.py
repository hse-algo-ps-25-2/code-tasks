import unittest

from abstract_schedule import AbstractSchedule
from constants import (
    SCHEDULE_ITEM_DOWNTIME_STR_TEMPL,
    SCHEDULE_ITEM_STR_TEMPL,
    SCHEDULE_STR_TEMPL,
    TASK_STR_TEMPL,
)
from errors import (
    ErrorMessages,
    ErrorTemplates,
    ScheduleArgumentError,
    ScheduleItemError,
    TaskArgumentError,
)
from schedule import Schedule
from schedule_item import ScheduleItem
from task import Task


class TestSchedule(unittest.TestCase):
    """Примеры ленточного расписания"""

    def test_class_inheritance(self):
        """Проверяет наследование от класса AbstractSchedule"""
        schedule = Schedule([Task("a", 1)], 1)
        self.assertIsInstance(schedule, AbstractSchedule)

    def test_none_tasks(self):
        """Проверяет выброс исключения при передаче некорректного параметра
        списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            Schedule(None, 1)
        self.assertEqual(ErrorMessages.TASKS_NOT_LIST, str(error.exception))

    def test_empty_tasks(self):
        """Проверяет выброс исключения при передаче пустого списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            Schedule([], 1)
        self.assertEqual(ErrorMessages.TASKS_EMPTY_LIST, str(error.exception))

    def test_tasks_contains_non_task(self):
        """Проверяет выброс исключения при передаче в списке задачи в
        некорректном формате."""
        tasks = [Task("a", 7), Task("b", 3), "non task object"]
        with self.assertRaises(ScheduleArgumentError) as error:
            Schedule(tasks, 1)
        self.assertEqual(ErrorTemplates.INVALID_TASK.format(2), str(error.exception))

    def test_not_int_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        tasks = [Task("a", 7), Task("b", 3)]
        schedule = Schedule(tasks, 1)
        incorrect_idx = [-1, 1.1, None, "str", []]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ErrorMessages.EXECUTOR_NOT_INT, str(error.exception))

    def test_out_of_range_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        tasks = [Task("a", 7), Task("b", 3)]
        schedule = Schedule(tasks, 1)
        incorrect_idx = [len(tasks), len(tasks) + 1]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(
                    ErrorMessages.EXECUTOR_OUT_OF_RANGE, str(error.exception)
                )

    def test_str(self):
        """Проверяет корректность приведения расписания к строковому типу."""
        task_a = Task("a", 1)
        schedule = Schedule([task_a], 1)
        str_schedule = SCHEDULE_STR_TEMPL.format(1.0, 1, 1)
        self.assertEqual(str_schedule, str(schedule))

    def test_single_task_single_executor(self):
        """Проверяет корректность составления расписания для одного исполнителя
        и одной задачи."""
        task_a = Task("a", 1)
        schedule = Schedule([task_a], 1)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration)]
        self.assertEqual(tuple([task_a]), schedule.tasks)
        self.assertEqual(1, schedule.task_count)
        self.assertEqual(1, schedule.executor_count)
        self.assertEqual(1, schedule.duration)
        self.assertCountEqual(executor1_schedule, schedule.get_schedule_for_executor(0))

    def test_double_task_single_executor(self):
        """Проверяет корректность составления расписания для одного исполнителя
        и двух задач."""
        task_a = Task("a", 2)
        task_b = Task("b", 1)
        schedule = Schedule([task_a, task_b], 1)
        executor1_schedule = [
            ScheduleItem(task_a, 0, task_a.duration),
            ScheduleItem(task_b, task_a.duration, task_b.duration),
        ]
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(1, schedule.executor_count)
        self.assertEqual(3, schedule.duration)
        self.assertCountEqual(executor1_schedule, schedule.get_schedule_for_executor(0))

    def test_single_task_double_executor(self):
        """Проверяет корректность составления расписания для двух исполнителей
        и одной задачи."""
        task_a = Task("a", 1)
        schedule = Schedule([task_a], 2)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration)]
        executor2_schedule = [ScheduleItem(None, 0, task_a.duration)]
        self.assertEqual(2, schedule.executor_count)
        self.assertEqual(1, schedule.duration)
        self.assertCountEqual(executor1_schedule, schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule, schedule.get_schedule_for_executor(1))

    def test_double_task_double_executor(self):
        """Проверяет корректность составления расписания для двух исполнителей
        и двух задач."""
        task_a = Task("a", 2)
        task_b = Task("b", 1)
        schedule = Schedule([task_a, task_b], 2)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration)]
        executor2_schedule = [
            ScheduleItem(task_b, 0, task_b.duration),
            ScheduleItem(None, 1, 1),
        ]
        self.assertEqual(2, schedule.executor_count)
        self.assertEqual(2, schedule.duration)
        self.assertCountEqual(executor1_schedule, schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule, schedule.get_schedule_for_executor(1))


class TestScheduleTeam(unittest.TestCase):
    """Дополнительные тесты команды для ленточного расписания"""

    def test_duration_balanced_between_executors(self):
        """Проверяет, что продолжительность расписания определяется средней
        загрузкой исполнителей, когда самая длинная задача её не превышает."""
        task_a = Task("a", 4)
        task_b = Task("b", 4)
        schedule = Schedule([task_a, task_b], 2)
        self.assertEqual(4, schedule.duration)
        executor1_schedule = [ScheduleItem(task_a, 0, task_a.duration)]
        executor2_schedule = [ScheduleItem(task_b, 0, task_b.duration)]
        self.assertCountEqual(executor1_schedule, schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule, schedule.get_schedule_for_executor(1))

    def test_duration_dominated_by_longest_task(self):
        """Проверяет, что продолжительность расписания определяется самой
        длинной задачей, когда она превышает среднюю загрузку исполнителей."""
        task_a = Task("a", 10)
        task_b = Task("b", 1)
        task_c = Task("c", 1)
        schedule = Schedule([task_a, task_b, task_c], 3)
        self.assertEqual(10, schedule.duration)
        # Вторая лента (задачи b и c) целиком попадает на второго
        # исполнителя, оставшееся окно заполняется простоем.
        executor2_schedule = [
            ScheduleItem(task_b, 0, task_b.duration),
            ScheduleItem(task_c, task_b.duration, task_c.duration),
            ScheduleItem(None, task_b.duration + task_c.duration, 8),
        ]
        executor3_schedule = [ScheduleItem(None, 0, schedule.duration)]
        self.assertCountEqual(executor2_schedule, schedule.get_schedule_for_executor(1))
        self.assertCountEqual(executor3_schedule, schedule.get_schedule_for_executor(2))

    def test_duration_fractional(self):
        """Проверяет, что продолжительность расписания может оказаться
        дробной, если суммарное время задач не делится нацело на количество
        исполнителей."""
        task_a = Task("a", 1)
        task_b = Task("b", 1)
        task_c = Task("c", 1)
        schedule = Schedule([task_a, task_b, task_c], 2)
        self.assertAlmostEqual(1.5, schedule.duration)

    def test_task_split_between_executors(self):
        """Проверяет, что одна задача может быть разделена между несколькими
        исполнителями при ленточном распределении."""
        task_a = Task("a", 1)
        task_b = Task("b", 3)
        task_c = Task("c", 2)
        schedule = Schedule([task_a, task_b, task_c], 2)
        self.assertEqual(3, schedule.duration)
        executor1_schedule = [
            ScheduleItem(task_a, 0, task_a.duration),
            ScheduleItem(task_b, task_a.duration, 2),
        ]
        executor2_schedule = [
            ScheduleItem(task_b, 0, 1),
            ScheduleItem(task_c, 1, task_c.duration),
        ]
        self.assertCountEqual(executor1_schedule, schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor2_schedule, schedule.get_schedule_for_executor(1))

    def test_no_downtime_when_balanced(self):
        """Проверяет, что при равномерном распределении задач простой в окне
        исполнителей отсутствует."""
        tasks = [Task("a", 1), Task("b", 1), Task("c", 1), Task("d", 1)]
        schedule = Schedule(tasks, 2)
        self.assertEqual(2, schedule.duration)
        for executor_index in range(schedule.executor_count):
            for piece in schedule.get_schedule_for_executor(executor_index):
                self.assertFalse(piece.is_downtime)

    def test_idle_executors_full_downtime(self):
        """Проверяет, что исполнители, которым не досталось ни одного
        фрагмента ленты, простаивают всё окно расписания."""
        task_a = Task("a", 2)
        task_b = Task("b", 2)
        schedule = Schedule([task_a, task_b], 4)
        self.assertEqual(2, schedule.duration)
        for executor_index in (2, 3):
            executor_schedule = schedule.get_schedule_for_executor(executor_index)
            self.assertEqual(1, len(executor_schedule))
            piece = executor_schedule[0]
            self.assertTrue(piece.is_downtime)
            self.assertEqual(0, piece.start)
            self.assertEqual(schedule.duration, piece.end)

    def test_schedule_coverage_property(self):
        """Проверяет инварианты ленточного расписания: элементы каждого
        исполнителя непрерывно покрывают окно расписания, а суммарные доли
        задач совпадают с их исходной продолжительностью."""
        tasks = [Task("a", 1), Task("b", 2), Task("c", 3)]
        schedule = Schedule(tasks, 2)

        total_duration = sum(task.duration for task in tasks)
        maximum_task_duration = max(task.duration for task in tasks)
        expected_duration = max(maximum_task_duration, total_duration / 2)
        self.assertEqual(expected_duration, schedule.duration)

        allocated_durations = {task.name: 0 for task in tasks}
        for executor_index in range(schedule.executor_count):
            position = 0
            for piece in schedule.get_schedule_for_executor(executor_index):
                self.assertEqual(position, piece.start)
                position = piece.end
                if not piece.is_downtime:
                    allocated_durations[piece.task_name] += piece.duration
            self.assertEqual(schedule.duration, position)

        for task in tasks:
            self.assertEqual(task.duration, allocated_durations[task.name])

    def test_three_task_three_executor_no_downtime(self):
        """Проверяет граничный случай, когда число задач совпадает с числом
        исполнителей и каждая задача целиком помещается в своё окно."""
        task_a = Task("a", 3)
        task_b = Task("b", 3)
        task_c = Task("c", 3)
        schedule = Schedule([task_a, task_b, task_c], 3)
        self.assertEqual(3, schedule.duration)
        expected_schedules = (
            [ScheduleItem(task_a, 0, task_a.duration)],
            [ScheduleItem(task_b, 0, task_b.duration)],
            [ScheduleItem(task_c, 0, task_c.duration)],
        )
        for executor_index, expected in enumerate(expected_schedules):
            self.assertCountEqual(
                expected, schedule.get_schedule_for_executor(executor_index)
            )


class TestTask(unittest.TestCase):
    name = "a"
    duration = 1
    task = Task(name, duration)

    def test_init_incorrect_name(self):
        """Проверяет выброс исключения при некорректном названии задачи"""
        incorrect_name_values = [None, 1, 1.1, True, []]
        for value in incorrect_name_values:
            with self.assertRaises(TaskArgumentError) as error:
                Task(value, self.duration)
            self.assertEqual(ErrorMessages.NOT_STR_NAME, str(error.exception))

    def test_init_empty_name(self):
        """Проверяет выброс исключения если название задачи является пустой
        строкой"""
        with self.assertRaises(TaskArgumentError) as error:
            Task("", self.duration)
        self.assertEqual(ErrorMessages.EMPTY_NAME, str(error.exception))

    def test_init_incorrect_duration(self):
        """Проверяет выброс исключения при некорректной продолжительности
        задачи"""
        incorrect_duration_values = [None, "1", []]
        for value in incorrect_duration_values:
            with self.assertRaises(TaskArgumentError) as error:
                Task(self.name, value)
            self.assertEqual(ErrorMessages.NOT_NUMBER_DUR, str(error.exception))

    def test_init_non_positive_duration(self):
        """Проверяет выброс исключения если продолжительность задачи меньше или
        равна нулю"""
        incorrect_name_values = [0, -1, -0.1]
        for value in incorrect_name_values:
            with self.assertRaises(TaskArgumentError) as error:
                Task(self.name, value)
            self.assertEqual(ErrorMessages.NEG_NUMBER_DUR, str(error.exception))

    def test_str(self):
        """Проверка приведения задачи к строковому типу"""
        self.assertEqual(
            TASK_STR_TEMPL.format(self.name, self.duration), str(self.task)
        )

    def test_name_property(self):
        """Проверка свойства name"""
        self.assertEqual(self.task.name, self.name)

    def test_duration_property(self):
        """Проверка свойства duration"""
        self.assertEqual(self.task.duration, self.duration)

    def test_eq(self):
        """Проверка операции эквивалентности заданий"""
        task1 = Task("a", 1)
        task2 = Task("a", 1)
        self.assertTrue(task1 == task2)
        self.assertTrue(hash(task1) == hash(task2))

    def test_not_eq(self):
        """Проверка операции неэквивалентности заданий"""
        task1 = Task("a", 1)
        task2 = Task("a", 1.1)
        self.assertTrue(task1 != task2)
        self.assertTrue(hash(task1) != hash(task2))


class TestScheduleItem(unittest.TestCase):
    def test_init_not_number_start(self):
        """Проверяет выброс исключения при некорректном указании времени
        начала выполнения задачи - передано не число"""
        incorrect_values = [None, "str", []]
        for value in incorrect_values:
            with self.assertRaises(ScheduleItemError) as error:
                ScheduleItem(None, value, 1)
            self.assertEqual(ErrorMessages.START_NOT_NUMBER, str(error.exception))

    def test_init_negative_start(self):
        """Проверяет выброс исключения при указании времени
        начала выполнения задачи меньше нуля"""
        with self.assertRaises(ScheduleItemError) as error:
            ScheduleItem(None, -1, 1)
        self.assertEqual(ErrorMessages.START_NEG_NUMBER, str(error.exception))

    def test_init_not_number_duration(self):
        """Проверяет выброс исключения при некорректном указании
        продолжительности выполнения задачи - передано не число"""
        incorrect_values = [None, "str", []]
        for value in incorrect_values:
            with self.assertRaises(ScheduleItemError) as error:
                ScheduleItem(None, 1, value)
            self.assertEqual(ErrorMessages.DUR_NOT_NUMBER, str(error.exception))

    def test_init_not_pos_duration(self):
        """Проверяет выброс исключения при указании продолжительности
        выполнения задачи меньше или равной нулю"""
        incorrect_values = [0, -1, -0.1]
        for value in incorrect_values:
            with self.assertRaises(ScheduleItemError) as error:
                ScheduleItem(None, 1, value)
            self.assertEqual(ErrorMessages.DUR_NOT_POS_NUMBER, str(error.exception))

    def test_init_integers(self):
        """Проверяет инициализацию объекта класса с целочисленными значениями"""
        task_name = "task"
        start = 0
        duration = 1
        row = ScheduleItem(Task(task_name, 1), start, duration)
        self.assertEqual(task_name, row.task_name)
        self.assertEqual(start, row.start)
        self.assertEqual(duration, row.duration)
        self.assertEqual(start + duration, row.end)
        self.assertFalse(row.is_downtime)

    def test_init_floats_downtime(self):
        """Проверяет инициализацию объекта класса с вещественными значениями
        и признаком простоя"""
        start = 1.1
        duration = 0.25
        item = ScheduleItem(None, start, duration)
        self.assertEqual("downtime", item.task_name)
        self.assertEqual(start, item.start)
        self.assertEqual(duration, item.duration)
        self.assertEqual(start + duration, item.end)
        self.assertTrue(item.is_downtime)
        err = SCHEDULE_ITEM_DOWNTIME_STR_TEMPL.format(start, start + duration)
        self.assertEqual(err, str(item))

    def test_str(self):
        """Проверка приведения объекта класса без простоя к строковому типу"""
        task_name = "task"
        start = 0
        duration = 1
        item = ScheduleItem(Task(task_name, duration), start, duration)
        str_item = SCHEDULE_ITEM_STR_TEMPL.format(task_name, start, start + duration)
        self.assertEqual(str_item, str(item))

    def test_str_downtime(self):
        """Проверка приведения объекта класса с простоем к строковому типу"""
        start = 1.1
        duration = 10
        item = ScheduleItem(None, start, duration)
        str_item = SCHEDULE_ITEM_DOWNTIME_STR_TEMPL.format(start, start + duration)
        self.assertEqual(str_item, str(item))


if __name__ == "__main__":
    unittest.main()
