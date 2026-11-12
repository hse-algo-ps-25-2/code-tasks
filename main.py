"""Пример ленточного расписания.

Методы __calculate_duration и __fill_schedule_for_each_executor
нужно реализовать в schedule.py.
"""

from schedule import Schedule
from task import Task


def main():
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
    print(schedule)
    for executor in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {executor + 1}:")
        for item in schedule.get_schedule_for_executor(executor):
            print(item)


if __name__ == "__main__":
    main()
