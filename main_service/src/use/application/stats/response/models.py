from dataclasses import dataclass


@dataclass(frozen=True)
class TaskProfileStatsResponse:
    task_type: int
    completed_percent: float
    user_completed_tasks: int
    all_tasks: int


@dataclass(frozen=True)
class TaskAdminStatsResponse:
    task_type: int
    all_tasks: int
    completed_percent: int
