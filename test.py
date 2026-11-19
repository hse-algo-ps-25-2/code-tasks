import unittest
from collections import Counter
from itertools import pairwise, permutations, product

from abstract_schedule import AbstractSchedule
from constants import (
    SCHEDULE_ITEM_DOWNTIME_STR_TEMPL,
    SCHEDULE_ITEM_STR_TEMPL,
    SCHEDULE_STR_TEMPL,
    STAGED_TASK_STR_TEMPL,
    TASK_STR_TEMPL,
)
from conveyor_schedule import ConveyorSchedule
from errors import (
    ErrorMessages,
    ErrorTemplates,
    ScheduleArgumentError,
    ScheduleItemError,
    TaskArgumentError,
)
from schedule_item import ScheduleItem
from staged_task import StagedTask
from task import Task


class TestConveyorSchedule(unittest.TestCase):
    """Примеры конвейерного расписания"""

    def test_class_inheritance(self):
        """Проверяет наследование от класса AbstractSchedule"""
        schedule = ConveyorSchedule([StagedTask("a", [1, 1])])
        self.assertIsInstance(schedule, AbstractSchedule)

    def test_none_tasks(self):
        """Проверяет выброс исключения при передаче некорректного параметра
        списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            ConveyorSchedule(None)
        self.assertEqual(ErrorMessages.TASKS_NOT_LIST, str(error.exception))

    def test_empty_tasks(self):
        """Проверяет выброс исключения при передаче пустого списка задач."""
        with self.assertRaises(ScheduleArgumentError) as error:
            ConveyorSchedule([])
        self.assertEqual(ErrorMessages.TASKS_EMPTY_LIST, str(error.exception))

    def test_tasks_contains_non_task(self):
        """Проверяет выброс исключения при передаче в списке задачи в
        некорректном формате."""
        tasks = [StagedTask("a", [1, 1]), StagedTask("b", [1, 1]), "non task object"]
        with self.assertRaises(ScheduleArgumentError) as error:
            ConveyorSchedule(tasks)
        self.assertEqual(ErrorTemplates.INVALID_TASK.format(2), str(error.exception))

    def test_not_int_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        tasks = [StagedTask("a", [1, 1]), StagedTask("b", [1, 1])]
        schedule = ConveyorSchedule(tasks)
        incorrect_idx = [-1, 1.1, None, "str", []]
        for idx in incorrect_idx:
            with self.subTest(idx=idx):
                with self.assertRaises(ScheduleArgumentError) as error:
                    schedule.get_schedule_for_executor(idx)
                self.assertEqual(ErrorMessages.EXECUTOR_NOT_INT, str(error.exception))

    def test_out_of_range_executor_idx(self):
        """Проверяет выброс исключения при передаче не корректного индекса
        исполнителя."""
        tasks = [StagedTask("a", [1, 1]), StagedTask("b", [1, 1])]
        schedule = ConveyorSchedule(tasks)
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
        tasks = [StagedTask("a", [1, 1]), StagedTask("b", [1, 1])]
        schedule = ConveyorSchedule(tasks)
        str_schedule = SCHEDULE_STR_TEMPL.format(3, 2, 2)
        self.assertEqual(str_schedule, str(schedule))

    def test_single_task(self):
        """Проверяет корректность составления расписания для одной задачи."""
        task_a = StagedTask("a", [1, 2])
        schedule = ConveyorSchedule([task_a])
        stage1_schedule = (
            ScheduleItem(task_a, 0, 1),
            ScheduleItem(None, 1, 2),
        )
        stage2_schedule = (
            ScheduleItem(None, 0, 1),
            ScheduleItem(task_a, 1, 2),
        )
        self.assertEqual(tuple([task_a]), schedule.tasks)
        self.assertEqual(1, schedule.task_count)
        self.assertEqual(3, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))

    def test_double_task(self):
        """Проверяет корректность составления расписания для двух задач."""
        task_a = StagedTask("a", [2, 1])
        task_b = StagedTask("b", [1, 2])
        schedule = ConveyorSchedule([task_a, task_b])
        stage1_schedule = (
            ScheduleItem(task_b, 0, 1),
            ScheduleItem(task_a, 1, 2),
            ScheduleItem(None, 3, 1),
        )
        stage2_schedule = (
            ScheduleItem(None, 0, 1),
            ScheduleItem(task_b, 1, 2),
            ScheduleItem(task_a, 3, 1),
        )
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(4, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))

    def test_equal_stages(self):
        """Проверяет расписание, в котором этапы одной задачи равны"""
        task_a = StagedTask("a", [2, 2])
        task_b = StagedTask("b", [3, 1])
        schedule = ConveyorSchedule([task_a, task_b])
        stage1_schedule = (
            ScheduleItem(task_a, 0, 2),
            ScheduleItem(task_b, 2, 3),
            ScheduleItem(None, 5, 1),
        )
        stage2_schedule = (
            ScheduleItem(None, 0, 2),
            ScheduleItem(task_a, 2, 2),
            ScheduleItem(None, 4, 1),
            ScheduleItem(task_b, 5, 1),
        )
        self.assertEqual(tuple([task_a, task_b]), schedule.tasks)
        self.assertEqual(2, schedule.task_count)
        self.assertEqual(6, schedule.duration)
        self.assertEqual(stage1_schedule, schedule.get_schedule_for_executor(0))
        self.assertEqual(stage2_schedule, schedule.get_schedule_for_executor(1))


class TestConveyorScheduleAdditional(unittest.TestCase):
    def test_tasks_must_be_a_list(self):
        tasks = [StagedTask("a", [1, 2])]
        invalid_values = (tuple(tasks), iter(tasks), {}, "tasks", 1, True)
        for invalid_tasks in invalid_values:
            with self.subTest(tasks=invalid_tasks):
                with self.assertRaises(ScheduleArgumentError) as error:
                    ConveyorSchedule(invalid_tasks)
                self.assertEqual(ErrorMessages.TASKS_NOT_LIST, str(error.exception))

    def test_plain_task_is_rejected(self):
        tasks = [StagedTask("a", [1, 2]), Task("b", 3)]
        with self.assertRaises(ScheduleArgumentError) as error:
            ConveyorSchedule(tasks)
        self.assertEqual(ErrorTemplates.INVALID_TASK.format(1), str(error.exception))

    def test_tasks_must_have_two_stages(self):
        for stage_durations in ([1], [1, 2, 3]):
            with self.subTest(stage_durations=stage_durations):
                tasks = [StagedTask("a", [1, 2]), StagedTask("b", stage_durations)]
                with self.assertRaises(ScheduleArgumentError) as error:
                    ConveyorSchedule(tasks)
                self.assertEqual(
                    ErrorTemplates.INVALID_STAGE_CNT.format(1), str(error.exception)
                )

    def test_executor_indices_do_not_depend_on_task_count(self):
        schedule = ConveyorSchedule([StagedTask("a", [1, 2])])
        self.assertEqual(2, schedule.executor_count)
        self.assertTrue(schedule.get_schedule_for_executor(1))
        with self.assertRaises(ScheduleArgumentError) as error:
            schedule.get_schedule_for_executor(2)
        self.assertEqual(ErrorMessages.EXECUTOR_OUT_OF_RANGE, str(error.exception))

    def test_both_johnson_groups(self):
        tasks = [
            StagedTask("a", [7, 2]),
            StagedTask("b", [3, 4]),
            StagedTask("c", [2, 5]),
            StagedTask("d", [4, 1]),
            StagedTask("e", [6, 6]),
            StagedTask("f", [5, 3]),
            StagedTask("g", [4, 5]),
        ]
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(("c", "b", "g", "e", "f", "a", "d"), self._order(schedule))
        self.assertEqual(32, schedule.duration)
        self._assert_valid_schedule(schedule)

    def test_only_first_group(self):
        tasks = [
            StagedTask("last", [5, 9]),
            StagedTask("first", [1, 6]),
            StagedTask("middle", [3, 3]),
        ]
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(("first", "middle", "last"), self._order(schedule))
        self._assert_valid_schedule(schedule)

    def test_only_second_group(self):
        tasks = [
            StagedTask("last", [3, 1]),
            StagedTask("first", [8, 5]),
            StagedTask("middle", [5, 2]),
        ]
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(("first", "middle", "last"), self._order(schedule))
        self._assert_valid_schedule(schedule)

    def test_equal_stages_belong_to_first_group(self):
        tasks = [
            StagedTask("long_first", [3, 8]),
            StagedTask("equal", [2, 2]),
            StagedTask("second_group", [4, 1]),
        ]
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(("equal", "long_first", "second_group"), self._order(schedule))

    def test_equal_sort_keys_keep_input_order(self):
        tasks = [
            StagedTask("second_a", [4, 1]),
            StagedTask("first_b", [1, 2]),
            StagedTask("second_b", [3, 1]),
            StagedTask("first_a", [1, 3]),
        ]
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(
            ("first_b", "first_a", "second_a", "second_b"), self._order(schedule)
        )
        self._assert_valid_schedule(schedule)

    def test_original_tasks_are_unchanged(self):
        tasks = [
            StagedTask("a", [7, 2]),
            StagedTask("b", [3, 4]),
            StagedTask("c", [2, 5]),
        ]
        original_tasks = tuple(tasks)
        original_stages = tuple(task.stage_durations for task in tasks)
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(original_tasks, tuple(tasks))
        self.assertEqual(original_tasks, schedule.tasks)
        self.assertEqual(original_stages, tuple(task.stage_durations for task in tasks))
        for original, stored in zip(original_tasks, schedule.tasks):
            self.assertIs(original, stored)

    def test_identical_tasks_are_not_lost(self):
        task = StagedTask("same", [1, 2])
        equal_task = StagedTask("same", [1, 2])
        schedule = ConveyorSchedule([task, equal_task, task])
        self.assertEqual(3, schedule.task_count)
        self.assertEqual(("same", "same", "same"), self._order(schedule))
        self.assertEqual(7, schedule.duration)
        self._assert_valid_schedule(schedule)

    def test_multiple_second_executor_downtimes(self):
        task_a = StagedTask("a", [5, 1])
        task_b = StagedTask("b", [6, 1])
        task_c = StagedTask("c", [7, 1])
        schedule = ConveyorSchedule([task_a, task_b, task_c])
        expected = (
            ScheduleItem(None, 0, 5),
            ScheduleItem(task_a, 5, 1),
            ScheduleItem(None, 6, 5),
            ScheduleItem(task_b, 11, 1),
            ScheduleItem(None, 12, 6),
            ScheduleItem(task_c, 18, 1),
        )
        self.assertEqual(expected, schedule.get_schedule_for_executor(1))
        self.assertEqual(19, schedule.duration)
        self._assert_valid_schedule(schedule)

    def test_busy_second_executor_has_only_initial_downtime(self):
        task_a = StagedTask("a", [1, 5])
        task_b = StagedTask("b", [2, 6])
        task_c = StagedTask("c", [3, 7])
        schedule = ConveyorSchedule([task_a, task_b, task_c])
        expected = (
            ScheduleItem(None, 0, 1),
            ScheduleItem(task_a, 1, 5),
            ScheduleItem(task_b, 6, 6),
            ScheduleItem(task_c, 12, 7),
        )
        self.assertEqual(expected, schedule.get_schedule_for_executor(1))
        self.assertEqual(19, schedule.duration)
        self._assert_valid_schedule(schedule)

    def test_fractional_durations(self):
        task_a = StagedTask("a", [1.5, 0.5])
        task_b = StagedTask("b", [0.25, 1.25])
        task_c = StagedTask("c", [0.75, 0.75])
        schedule = ConveyorSchedule([task_a, task_b, task_c])
        expected = (
            ScheduleItem(None, 0, 0.25),
            ScheduleItem(task_b, 0.25, 1.25),
            ScheduleItem(task_c, 1.5, 0.75),
            ScheduleItem(None, 2.25, 0.25),
            ScheduleItem(task_a, 2.5, 0.5),
        )
        self.assertEqual(expected, schedule.get_schedule_for_executor(1))
        self.assertEqual(3, schedule.duration)
        self._assert_valid_schedule(schedule)

    def test_decimal_durations(self):
        tasks = [
            StagedTask("a", [0.1, 0.2]),
            StagedTask("b", [0.3, 0.1]),
            StagedTask("c", [0.2, 0.4]),
        ]
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(("a", "c", "b"), self._order(schedule))
        self.assertAlmostEqual(0.8, schedule.duration)
        self._assert_valid_schedule(schedule)

    def test_large_integer_durations_remain_exact(self):
        large_duration = 10**20
        tasks = [
            StagedTask("a", [large_duration + 1, 1]),
            StagedTask("b", [1, large_duration + 3]),
        ]
        schedule = ConveyorSchedule(tasks)
        self.assertEqual(large_duration + 5, schedule.duration)
        self.assertIsInstance(schedule.duration, int)
        self._assert_valid_schedule(schedule)

    def test_optimality_against_all_permutations(self):
        duration_pairs = ((1, 1), (1, 3), (3, 1), (2, 2), (2, 3), (3, 2))
        for task_count in range(1, 5):
            for stages in product(duration_pairs, repeat=task_count):
                with self.subTest(stages=stages):
                    tasks = [
                        StagedTask(f"task_{index}", list(durations))
                        for index, durations in enumerate(stages)
                    ]
                    schedule = ConveyorSchedule(tasks)
                    minimum_duration = min(
                        self._duration_for_order(order) for order in permutations(tasks)
                    )
                    self.assertEqual(minimum_duration, schedule.duration)
                    self._assert_valid_schedule(schedule)

    @staticmethod
    def _order(schedule):
        return tuple(
            item.task_name
            for item in schedule.get_schedule_for_executor(0)
            if not item.is_downtime
        )

    @staticmethod
    def _duration_for_order(tasks):
        """Считает длительность для заданного порядка через критический путь"""
        return max(
            sum(task.stage_duration(0) for task in tasks[:boundary])
            + sum(task.stage_duration(1) for task in tasks[boundary - 1 :])
            for boundary in range(1, len(tasks) + 1)
        )

    def _assert_valid_schedule(self, schedule):
        rows = tuple(
            schedule.get_schedule_for_executor(executor_idx)
            for executor_idx in range(schedule.executor_count)
        )
        self.assertEqual(2, len(rows))
        for executor_idx, row in enumerate(rows):
            self.assertIsInstance(row, tuple)
            self.assertEqual(0, row[0].start)
            self.assertAlmostEqual(schedule.duration, row[-1].end)
            for item in row:
                self.assertGreater(item.duration, 0)
            for previous, current in pairwise(row):
                self.assertAlmostEqual(previous.end, current.start)
            actual_tasks = Counter(
                (item.task_name, item.duration) for item in row if not item.is_downtime
            )
            expected_tasks = Counter(
                (task.name, task.stage_duration(executor_idx))
                for task in schedule.tasks
            )
            self.assertEqual(expected_tasks, actual_tasks)

        self.assertTrue(rows[0][-1].is_downtime)
        self.assertFalse(any(item.is_downtime for item in rows[0][:-1]))
        first_stages = tuple(item for item in rows[0] if not item.is_downtime)
        second_stages = tuple(item for item in rows[1] if not item.is_downtime)
        self.assertEqual(
            tuple(item.task_name for item in first_stages),
            tuple(item.task_name for item in second_stages),
        )
        for first_stage, second_stage in zip(first_stages, second_stages):
            self.assertGreaterEqual(second_stage.start, first_stage.end)


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


class TestStagedTask(unittest.TestCase):
    name = "a"
    stage_0_duration = 1
    stage_1_duration = 2
    stage_2_duration = 3
    stage_durations = [stage_0_duration, stage_1_duration, stage_2_duration]
    task = StagedTask(name, stage_durations)

    def test_class_inheritance(self):
        """Проверяет наследование от класса Task"""
        self.assertIsInstance(self.task, Task)

    def test_init_incorrect_name(self):
        """Проверяет выброс исключения при некорректном названии задачи"""
        incorrect_name_values = [None, 1, 1.1, True, []]
        for value in incorrect_name_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                StagedTask(value, self.stage_durations)
            self.assertEqual(ErrorMessages.NOT_STR_NAME, str(error.exception))

    def test_init_empty_name(self):
        """Проверяет выброс исключения если название задачи является пустой
        строкой"""
        with self.assertRaises(TaskArgumentError) as error:
            StagedTask("", self.stage_durations)
        self.assertEqual(ErrorMessages.EMPTY_NAME, str(error.exception))

    def test_init_not_list_duration(self):
        """Проверяет выброс исключения при некорректном типе данных списка
        этапов задачи"""
        incorrect_durations_values = [None, "1", {}]
        for value in incorrect_durations_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                StagedTask(self.name, value)
            self.assertEqual(ErrorMessages.NOT_LIST_DUR, str(error.exception))

    def test_init_empty_list_duration(self):
        """Проверяет выброс исключения при передаче пустого списка этапов
        задачи"""
        with self.assertRaises(TaskArgumentError) as error:
            StagedTask(self.name, [])
        self.assertEqual(ErrorMessages.EMPTY_LIST_DUR, str(error.exception))

    def test_init_incorrect_duration(self):
        """Проверяет выброс исключения при некорректной продолжительности
        этапа задачи"""
        incorrect_duration_values = [None, "1", []]
        for value in incorrect_duration_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                stage_durations = [self.stage_0_duration, value]
                StagedTask(self.name, stage_durations)
            self.assertEqual(
                ErrorTemplates.NOT_NUMBER_DUR.format(1), str(error.exception)
            )

    def test_init_non_positive_duration(self):
        """Проверяет выброс исключения если продолжительность этапа задачи
        меньше или равна нулю"""
        incorrect_duration_values = [0, -1, -0.1]
        for value in incorrect_duration_values:
            with (
                self.subTest(name=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                stage_durations = [self.stage_0_duration, value]
                StagedTask(self.name, stage_durations)
            self.assertEqual(
                ErrorTemplates.NEG_NUMBER_DUR.format(1), str(error.exception)
            )

    def test_str(self):
        """Проверка приведения задачи к строковому типу"""
        task_str = STAGED_TASK_STR_TEMPL.format(
            self.name, sum(self.stage_durations), len(self.stage_durations)
        )
        self.assertEqual(task_str, str(self.task))

    def test_name_property(self):
        """Проверка свойства name"""
        self.assertEqual(self.task.name, self.name)

    def test_duration_property(self):
        """Проверка свойства duration"""
        self.assertEqual(self.task.duration, sum(self.stage_durations))

    def test_stage_count_property(self):
        """Проверка свойства stage_count"""
        self.assertEqual(self.task.stage_count, len(self.stage_durations))

    def test_stage_durations_property(self):
        """Проверка свойства stage_count"""
        self.assertEqual(self.task.stage_durations, tuple(self.stage_durations))

    def test_stage_duration(self):
        """Проверка метода получения длительности этапа"""
        self.assertEqual(self.task.stage_duration(1), self.stage_1_duration)

    def test_stage_duration_not_int_idx(self):
        """Проверка выброса исключения при нечисловом индексе этапа"""
        incorrect_idx_values = [None, "1", -1, 1.1, {}]
        for value in incorrect_idx_values:
            with (
                self.subTest(value=value),
                self.assertRaises(TaskArgumentError) as error,
            ):
                self.task.stage_duration(value)
            self.assertEqual(ErrorMessages.STAGE_NOT_INT, str(error.exception))

    def test_stage_duration_incorrect_idx(self):
        """Проверка выброса исключения при некорректном индексе этапа"""
        with self.assertRaises(TaskArgumentError) as error:
            self.task.stage_duration(len(self.stage_durations) + 1)
        self.assertEqual(ErrorMessages.STAGE_OUT_OF_RANGE, str(error.exception))

    def test_eq(self):
        """Проверка операции эквивалентности заданий"""
        task1 = StagedTask("a", [1, 1, 1])
        task2 = StagedTask("a", [1, 1, 1])
        self.assertTrue(task1 == task2)
        self.assertTrue(hash(task1) == hash(task2))

    def test_not_eq(self):
        """Проверка операции неэквивалентности заданий"""
        task1 = StagedTask("a", [1.1, 1, 1])
        task2 = StagedTask("a", [1, 1, 1])
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
