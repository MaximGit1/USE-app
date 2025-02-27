from dataclasses import (
    dataclass,
)

from use.entities.common.models import Entity
from use.entities.task.enums import TaskTypeEnum
from use.entities.task.value_objects import (
    TaskAnswer,
    TaskBody,
    TaskCodeBody,
    TaskID,
    TaskTimeLimit,
)
from use.entities.user.value_objects import UserID


@dataclass(
    slots=True,
    kw_only=True,
)
class Task(Entity[TaskID]):
    type: TaskTypeEnum
    body: TaskBody
    answer: TaskAnswer
    time_limit: TaskTimeLimit


@dataclass(
    slots=True,
    kw_only=True,
)
class TaskCompleted(Entity[TaskID]):
    task_id: TaskID
    user_id: UserID
    code: TaskCodeBody
    completed_time: float
