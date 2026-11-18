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

    def test_task_splitting_between_executors(self):
        """Проверяет разделение задачи между двумя исполнителями."""
        task_a = Task("A", 4)
        task_b = Task("B", 4)
        task_c = Task("C", 4)
        schedule = Schedule([task_a, task_b, task_c], 2)
        self.assertEqual(6.0, schedule.duration)
        self.assertEqual(
            (
                ScheduleItem(task_a, 0, 4),
                ScheduleItem(task_b, 4, 2),
            ),
            schedule.get_schedule_for_executor(0),
        )
        self.assertEqual(
            (
                ScheduleItem(task_b, 0, 2),
                ScheduleItem(task_c, 2, 4),
            ),
            schedule.get_schedule_for_executor(1),
        )

    def test_fractional_task_durations(self):
        """Проверяет распределение задач с дробной продолжительностью."""
        task_a = Task("A", 1.5)
        task_b = Task("B", 1.5)
        task_c = Task("C", 1.5)
        schedule = Schedule([task_a, task_b, task_c], 2)
        self.assertEqual(2.25, schedule.duration)
        self.assertEqual(
            (
                ScheduleItem(task_a, 0, 1.5),
                ScheduleItem(task_b, 1.5, 0.75),
            ),
            schedule.get_schedule_for_executor(0),
        )
        self.assertEqual(
            (
                ScheduleItem(task_b, 0, 0.75),
                ScheduleItem(task_c, 0.75, 1.5),
            ),
            schedule.get_schedule_for_executor(1),
        )

    def test_unused_executors(self):
        """Проверяет простой полностью свободных исполнителей."""
        task_a = Task("A", 5)
        schedule = Schedule([task_a], 4)
        self.assertEqual(5.0, schedule.duration)
        self.assertEqual(
            (ScheduleItem(task_a, 0, 5),),
            schedule.get_schedule_for_executor(0),
        )
        for executor_idx in range(1, 4):
            with self.subTest(executor_idx=executor_idx):
                self.assertEqual(
                    (ScheduleItem(None, 0, 5),),
                    schedule.get_schedule_for_executor(executor_idx),
                )

    def test_very_short_task(self):
        """Проверяет, что очень короткая задача не теряется."""
        task = Task("tiny", 1e-10)
        schedule = Schedule([task], 1)
        self.assertEqual(1e-10, schedule.duration)
        self.assertEqual(
            (ScheduleItem(task, 0, 1e-10),),
            schedule.get_schedule_for_executor(0),
        )

    def test_small_task_after_large_task(self):
        """Проверяет сохранение короткой задачи после длинной."""
        task_a = Task("A", 1)
        task_b = Task("B", 1e-10)
        schedule = Schedule([task_a, task_b], 1)
        items = schedule.get_schedule_for_executor(0)
        self.assertEqual(2, len(items))
        self.assertEqual("A", items[0].task_name)
        self.assertEqual("B", items[1].task_name)
        self.assertAlmostEqual(1e-10, items[1].duration, delta=1e-15)

    def test_floating_point_precision(self):
        """Проверяет работу с дробными числами и погрешностями float."""
        tasks = [
            Task("A", 0.1),
            Task("B", 0.2),
            Task("C", 0.3),
        ]
        schedule = Schedule(tasks, 2)
        self.assertAlmostEqual(0.3, schedule.duration)
        for executor_idx in range(schedule.executor_count):
            items = schedule.get_schedule_for_executor(executor_idx)
            self.assertAlmostEqual(
                schedule.duration,
                sum(item.duration for item in items),
            )

    def test_multiple_task_splits(self):
        """Проверяет несколько разрезаний ленты."""
        tasks = [Task(name, 4) for name in "ABCDE"]
        schedule = Schedule(tasks, 3)
        self.assertAlmostEqual(20 / 3, schedule.duration)
        for executor_idx in range(schedule.executor_count):
            items = schedule.get_schedule_for_executor(executor_idx)
            self.assertTrue(items)
            self.assertAlmostEqual(0, items[0].start)
            self.assertAlmostEqual(schedule.duration, items[-1].end)

    def test_schedule_covers_full_duration(self):
        """Проверяет непрерывность расписания каждого исполнителя."""
        tasks = [Task("A", 7), Task("B", 3), Task("C", 2)]
        schedule = Schedule(tasks, 5)
        for executor_idx in range(schedule.executor_count):
            items = schedule.get_schedule_for_executor(executor_idx)
            self.assertTrue(items)
            self.assertAlmostEqual(0, items[0].start)
            self.assertAlmostEqual(schedule.duration, items[-1].end)
            for previous, current in zip(items, items[1:]):
                self.assertAlmostEqual(previous.end, current.start)

    def test_task_parts_do_not_overlap(self):
        """Проверяет отсутствие одновременного выполнения одной задачи."""
        tasks = [Task("A", 4), Task("B", 4), Task("C", 4)]
        schedule = Schedule(tasks, 2)
        for task in tasks:
            intervals = []
            for executor_idx in range(schedule.executor_count):
                for item in schedule.get_schedule_for_executor(executor_idx):
                    if item.task_name == task.name:
                        intervals.append((item.start, item.end))
            intervals.sort()
            for previous, current in zip(intervals, intervals[1:]):
                self.assertLessEqual(previous[1], current[0])

    def test_decimal_precision_multiple_tasks(self):
        """Проверяет точность распределения десяти дробных задач."""
        tasks = [Task(f"T{i}", 0.1) for i in range(10)]
        schedule = Schedule(tasks, 3)

        self.assertAlmostEqual(1 / 3, schedule.duration)

        total_work = sum(
            item.duration
            for i in range(schedule.executor_count)
            for item in schedule.get_schedule_for_executor(i)
            if not item.is_downtime
        )

        self.assertAlmostEqual(1.0, total_work)

    def test_decimal_precision_tiny_tasks(self):
        """Проверяет распределение очень коротких задач."""
        tasks = [Task(f"T{i}", 1e-12) for i in range(10)]
        schedule = Schedule(tasks, 3)

        total_work = sum(
            item.duration
            for i in range(schedule.executor_count)
            for item in schedule.get_schedule_for_executor(i)
            if not item.is_downtime
        )

        self.assertAlmostEqual(1e-11, total_work, delta=1e-20)

    def test_all_tasks_fully_executed(self):
        """Проверяет сохранение длительности каждой задачи."""
        tasks = [Task(f"T{i}", 0.1) for i in range(10)]
        schedule = Schedule(tasks, 3)

        for task in tasks:
            total_duration = sum(
                item.duration
                for executor_idx in range(schedule.executor_count)
                for item in schedule.get_schedule_for_executor(executor_idx)
                if item.task_name == task.name
            )

            self.assertAlmostEqual(
                task.duration,
                total_duration,
                delta=1e-12,
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
