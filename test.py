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

    def test_duration_matches_theoretical_formula(self):
        """Проверяет, что duration = max(t_max, sum/k) на нескольких наборах задач."""
        cases = [
            ([Task("a", 1)], 1, 1),
            ([Task("a", 2), Task("b", 1)], 2, 2),
            ([Task("a", 2), Task("b", 1)], 1, 3),
            (
                [
                    Task("a", 5),
                    Task("b", 2),
                    Task("c", 4),
                    Task("d", 3),
                    Task("e", 7),
                    Task("f", 6),
                ],
                3,
                9,
            ),
            (
                [
                    Task("a", 5),
                    Task("b", 2),
                    Task("c", 4),
                    Task("d", 3),
                    Task("e", 13),
                    Task("f", 6),
                ],
                3,
                13,
            ),
        ]
        for tasks, k, expected in cases:
            with self.subTest(k=k, n=len(tasks)):
                schedule = Schedule(tasks, k)
                self.assertAlmostEqual(expected, schedule.duration)

    def test_no_downtime_when_balanced(self):
        """Проверяет, что при sum/k = t_max окна заняты полностью, без простоев."""
        task_a = Task("a", 2)
        task_b = Task("b", 2)
        task_c = Task("c", 2)
        schedule = Schedule([task_a, task_b, task_c], 3)
        self.assertAlmostEqual(2, schedule.duration)
        for idx, task in enumerate([task_a, task_b, task_c]):
            with self.subTest(executor_idx=idx):
                self.assertCountEqual(
                    (ScheduleItem(task, 0, 2),),
                    schedule.get_schedule_for_executor(idx),
                )

    def test_task_ends_exactly_on_boundary(self):
        """Проверяет, что задача, заканчивающаяся на границе окна, не создаёт
        нулевой ScheduleItem."""
        task_a = Task("a", 2)
        task_b = Task("b", 2)
        schedule = Schedule([task_a, task_b], 2)
        self.assertAlmostEqual(2, schedule.duration)
        self.assertCountEqual(
            (ScheduleItem(task_a, 0, 2),),
            schedule.get_schedule_for_executor(0),
        )
        self.assertCountEqual(
            (ScheduleItem(task_b, 0, 2),),
            schedule.get_schedule_for_executor(1),
        )

    def test_task_split_across_executors(self):
        """Проверяет разрезание одной задачи между двумя исполнителями."""
        task_a = Task("a", 10)
        task_b = Task("b", 10)
        task_c = Task("c", 10)
        schedule = Schedule([task_a, task_b, task_c], 2)
        self.assertAlmostEqual(15, schedule.duration)
        executor0 = [
            ScheduleItem(task_a, 0, 10),
            ScheduleItem(task_b, 10, 5),
        ]
        executor1 = [
            ScheduleItem(task_b, 0, 5),
            ScheduleItem(task_c, 5, 10),
        ]
        self.assertCountEqual(executor0, schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor1, schedule.get_schedule_for_executor(1))

    def test_long_task_dominates(self):
        """Проверяет, что при T_opt = t_max хвост окна записывается простоем."""
        task_a = Task("a", 3)
        task_b = Task("b", 13)
        task_c = Task("c", 4)
        schedule = Schedule([task_a, task_b, task_c], 3)
        self.assertAlmostEqual(13, schedule.duration)
        executor0 = [
            ScheduleItem(task_a, 0, 3),
            ScheduleItem(task_b, 3, 10),
        ]
        executor1 = [
            ScheduleItem(task_b, 0, 3),
            ScheduleItem(task_c, 3, 4),
            ScheduleItem(None, 7, 6),
        ]
        executor2 = [ScheduleItem(None, 0, 13)]
        self.assertCountEqual(executor0, schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor1, schedule.get_schedule_for_executor(1))
        self.assertCountEqual(executor2, schedule.get_schedule_for_executor(2))

    def test_many_executors_few_tasks(self):
        """Проверяет, что лишние исполнители простаивают всё окно."""
        task_a = Task("a", 1)
        schedule = Schedule([task_a], 5)
        self.assertAlmostEqual(1, schedule.duration)
        self.assertEqual(5, schedule.executor_count)
        self.assertCountEqual(
            (ScheduleItem(task_a, 0, 1),),
            schedule.get_schedule_for_executor(0),
        )
        for idx in range(1, 5):
            with self.subTest(executor_idx=idx):
                self.assertCountEqual(
                    (ScheduleItem(None, 0, 1),),
                    schedule.get_schedule_for_executor(idx),
                )

    def test_float_durations(self):
        """Проверяет нарезку на окна при дробных длительностях задач."""
        task_a = Task("a", 1.5)
        task_b = Task("b", 2.5)
        schedule = Schedule([task_a, task_b], 2)
        self.assertAlmostEqual(2.5, schedule.duration)
        executor0 = [
            ScheduleItem(task_a, 0, 1.5),
            ScheduleItem(task_b, 1.5, 1.0),
        ]
        executor1 = [
            ScheduleItem(task_b, 0, 1.5),
            ScheduleItem(None, 1.5, 1.0),
        ]
        self.assertCountEqual(executor0, schedule.get_schedule_for_executor(0))
        self.assertCountEqual(executor1, schedule.get_schedule_for_executor(1))

    def test_each_executor_fills_full_window(self):
        """Проверяет, что элементы расписания покрывают окно [0, T_opt] без
        пропусков."""
        tasks = [
            Task("a", 3),
            Task("b", 4),
            Task("c", 6),
            Task("d", 7),
            Task("e", 7),
            Task("f", 9),
            Task("g", 10),
            Task("h", 12),
            Task("i", 17),
        ]
        schedule = Schedule(tasks, 5)
        for executor_idx in range(schedule.executor_count):
            with self.subTest(executor_idx=executor_idx):
                items = schedule.get_schedule_for_executor(executor_idx)
                self.assertTrue(len(items) > 0)
                self.assertAlmostEqual(0, items[0].start)
                self.assertAlmostEqual(schedule.duration, items[-1].end)
                for prev, curr in zip(items, items[1:]):
                    self.assertAlmostEqual(prev.end, curr.start)
                total = sum(item.duration for item in items)
                self.assertAlmostEqual(schedule.duration, total)

    def test_total_work_conserved(self):
        """Проверяет, что суммарное рабочее время равно сумме длительностей задач."""
        tasks = [
            Task("a", 3),
            Task("b", 4),
            Task("c", 6),
            Task("d", 7),
            Task("e", 7),
            Task("f", 9),
            Task("g", 10),
            Task("h", 12),
            Task("i", 17),
        ]
        schedule = Schedule(tasks, 5)
        total_task_time = 0
        for executor_idx in range(schedule.executor_count):
            for item in schedule.get_schedule_for_executor(executor_idx):
                if not item.is_downtime:
                    total_task_time += item.duration
        self.assertAlmostEqual(sum(task.duration for task in tasks), total_task_time)

    def test_tasks_property_is_tuple(self):
        """Проверяет, что свойство tasks возвращает tuple."""
        tasks = [Task("a", 1), Task("b", 2)]
        schedule = Schedule(tasks, 1)
        self.assertIsInstance(schedule.tasks, tuple)
        self.assertEqual(2, len(schedule.tasks))

    def test_executor_schedule_is_chronological(self):
        """Проверяет, что элементы расписания исполнителя идут по возрастанию
        времени."""
        task_a = Task("a", 2)
        task_b = Task("b", 1)
        schedule = Schedule([task_a, task_b], 1)
        self.assertEqual(
            (ScheduleItem(task_a, 0, 2), ScheduleItem(task_b, 2, 1)),
            schedule.get_schedule_for_executor(0),
        )

    def test_two_partial_tasks_in_one_window(self):
        """Проверяет, что в одном окне может быть два разрезанных задания."""
        tasks = [Task(name, 2) for name in ("a", "b", "c", "d", "e")]
        schedule = Schedule(tasks, 3)
        items = schedule.get_schedule_for_executor(1)
        self.assertEqual(3, len(items))
        self.assertEqual("b", items[0].task_name)
        self.assertEqual("c", items[1].task_name)
        self.assertEqual("d", items[2].task_name)
        self.assertAlmostEqual(0, items[0].start)
        self.assertAlmostEqual(schedule.duration, items[-1].end)

    def test_tasks_order_preserved(self):
        """Проверяет, что порядок задач из конструктора не меняется."""
        task_c = Task("c", 3)
        task_a = Task("a", 1)
        task_b = Task("b", 2)
        schedule = Schedule([task_c, task_a, task_b], 1)
        self.assertEqual((task_c, task_a, task_b), schedule.tasks)

    def test_get_schedule_returns_tuple(self):
        """Проверяет, что get_schedule_for_executor возвращает tuple."""
        schedule = Schedule([Task("a", 1)], 1)
        self.assertIsInstance(schedule.get_schedule_for_executor(0), tuple)

    def test_abstract_schedule_cannot_be_instantiated(self):
        """Проверяет, что AbstractSchedule нельзя создать напрямую."""
        with self.assertRaises(TypeError):
            AbstractSchedule([Task("a", 1)], 1)

    def test_zero_executor_count_raises(self):
        """Проверяет выброс ZeroDivisionError при нулевом числе исполнителей."""
        with self.assertRaises(ZeroDivisionError):
            Schedule([Task("a", 1)], 0)


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

    def test_eq_with_falsy_non_task(self):
        """Проверяет сравнение задачи с None, 0, '' и [] без исключения."""
        task = Task("a", 1)
        for other in (None, 0, "", []):
            with self.subTest(other=other):
                self.assertFalse(task == other)
                self.assertTrue(task != other)

    def test_positive_float_duration(self):
        """Проверяет инициализацию задачи с положительной дробной длительностью."""
        task = Task("a", 0.5)
        self.assertEqual(0.5, task.duration)


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

    def test_eq(self):
        """Проверяет равенство и одинаковый хеш у равных элементов расписания."""
        task = Task("a", 1)
        item1 = ScheduleItem(task, 0, 1)
        item2 = ScheduleItem(task, 0, 1)
        self.assertTrue(item1 == item2)
        self.assertTrue(hash(item1) == hash(item2))

    def test_not_eq(self):
        """Проверяет неравенство элементов расписания с разным началом."""
        task = Task("a", 1)
        item1 = ScheduleItem(task, 0, 1)
        item2 = ScheduleItem(task, 1, 1)
        self.assertTrue(item1 != item2)
        self.assertTrue(hash(item1) != hash(item2))

    def test_end_for_downtime(self):
        """Проверяет вычисление end для элемента расписания с простоем."""
        item = ScheduleItem(None, 2.5, 1.5)
        self.assertAlmostEqual(4.0, item.end)

    def test_start_zero_float(self):
        """Проверяет инициализацию элемента расписания с нулевым дробным
        началом."""
        item = ScheduleItem(None, 0.0, 1)
        self.assertEqual(0.0, item.start)

    def test_negative_float_start(self):
        """Проверяет выброс исключения при отрицательном дробном начале."""
        with self.assertRaises(ScheduleItemError) as error:
            ScheduleItem(None, -0.5, 1)
        self.assertEqual(ErrorMessages.START_NEG_NUMBER, str(error.exception))

    def test_negative_float_duration(self):
        """Проверяет выброс исключения при отрицательной дробной длительности."""
        with self.assertRaises(ScheduleItemError) as error:
            ScheduleItem(None, 0, -0.5)
        self.assertEqual(ErrorMessages.DUR_NOT_POS_NUMBER, str(error.exception))


if __name__ == "__main__":
    unittest.main()
