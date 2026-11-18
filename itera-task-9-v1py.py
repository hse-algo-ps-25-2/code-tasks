from abstract_schedule import AbstractSchedule
from errors import (
    ErrorMessages,
    ErrorTemplates,
    ScheduleArgumentError,
)
from schedule_item import ScheduleItem
from staged_task import StagedTask


class ConveyorSchedule(AbstractSchedule):
    def __init__(self, tasks: list[StagedTask]):
        ConveyorSchedule.__validate_params(tasks)
        super().__init__(tasks, 2)

  
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    @property
    def duration(self) -> float:
        return self._executor_schedule[0][-1].end

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        first_row = self._executor_schedule[0]
        second_row = self._executor_schedule[1]

         first_end = 0
        second_end = 0

        for task in tasks:
            stage1 = task.stage_duration(0)
            stage2 = task.stage_duration(1)

            first_row.append(ScheduleItem(task, first_end, stage1))
            first_end += stage1

  
            start = max(first_end, second_end)
            if start > second_end:
                second_row.append(ScheduleItem(None, second_end, start - second_end))
            second_row.append(ScheduleItem(task, start, stage2))
            second_end = start + stage2

 
        if second_end > first_end:
            first_row.append(ScheduleItem(None, first_end, second_end - first_end))

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:

        first_group = [
            task for task in tasks if task.stage_duration(0) <= task.stage_duration(1)
        ]
        second_group = [
            task for task in tasks if task.stage_duration(0) > task.stage_duration(1)
        ]

        first_group = sorted(first_group, key=lambda task: task.stage_duration(0))
        second_group = sorted(
            second_group, key=lambda task: task.stage_duration(1), reverse=True
        )
        return first_group + second_group

    @staticmethod
    def __validate_params(tasks: list[StagedTask]) -> None:
        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ErrorMessages.TASKS_EMPTY_LIST)
        for idx, value in enumerate(tasks):
            if not isinstance(value, StagedTask):
                raise ScheduleArgumentError(ErrorTemplates.INVALID_TASK.format(idx))
            if value.stage_count != 2:
                raise ScheduleArgumentError(
                    ErrorTemplates.INVALID_STAGE_CNT.format(idx)
                )
