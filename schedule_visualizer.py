from io import BytesIO

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from abstract_schedule import AbstractSchedule


class ScheduleVisualizer:
    """Создаёт диаграмму Ганта для расписания исполнителей."""

    def __init__(self, schedule: AbstractSchedule):
        self._schedule = schedule

    def to_png(self) -> bytes:
        """Возвращает PNG-изображение диаграммы Ганта в памяти."""
        fig, ax = plt.subplots(figsize=(11, 5))

        task_names = [task.name for task in self._schedule.tasks]
        colors = plt.get_cmap("tab20").resampled(max(len(task_names), 1))
        task_colors = {name: colors(idx) for idx, name in enumerate(task_names)}

        for executor_idx in range(self._schedule.executor_count):
            items = self._schedule.get_schedule_for_executor(executor_idx)

            for item in items:
                color = "#D3D3D3" if item.is_downtime else task_colors[item.task_name]

                ax.barh(
                    executor_idx,
                    item.duration,
                    left=item.start,
                    height=0.6,
                    color=color,
                    edgecolor="black",
                )

                ax.text(
                    item.start + item.duration / 2,
                    executor_idx,
                    item.task_name,
                    ha="center",
                    va="center",
                    fontsize=9,
                )

        ax.set_yticks(range(self._schedule.executor_count))
        ax.set_yticklabels(
            [f"Исполнитель {idx + 1}" for idx in range(self._schedule.executor_count)]
        )
        ax.invert_yaxis()
        ax.set_xlabel("Время")
        ax.set_title("Диаграмма Ганта")
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        ax.set_axisbelow(True)

        fig.tight_layout()

        buffer = BytesIO()

        try:
            fig.savefig(buffer, format="png", dpi=150)
            return buffer.getvalue()
        finally:
            plt.close(fig)
            buffer.close()
