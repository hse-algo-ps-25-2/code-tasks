import unittest

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
