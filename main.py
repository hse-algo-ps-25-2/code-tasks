"""Пример конвейерного расписания.

Методы __sort_tasks и __fill_schedule нужно реализовать
в conveyor_schedule.py.
"""

from conveyor_schedule import ConveyorSchedule
from staged_task import StagedTask


def main():
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
    print(schedule)
    for executor in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {executor + 1}:")
        for item in schedule.get_schedule_for_executor(executor):
            print(item)


if __name__ == "__main__":
    main()
