from pathlib import Path

from schedule import Schedule
from schedule_visualizer import ScheduleVisualizer
from task import Task


def main() -> None:
    tasks = [
        Task("A", 4),
        Task("B", 4),
        Task("C", 4),
        Task("D", 2),
    ]

    schedule = Schedule(tasks, 3)

    visualizer = ScheduleVisualizer(schedule)
    image = visualizer.to_png()

    output_path = Path("gantt_chart.png")
    output_path.write_bytes(image)

    print(f"Диаграмма сохранена: {output_path.resolve()}")


if __name__ == "__main__":
    main()
