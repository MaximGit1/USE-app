from dataclasses import dataclass
from typing import Any

from use.application.common.request.models import SortOrder
from use.entities.task.enums import TaskTypeEnum


@dataclass
class SearchFilters:
    order_by: TaskTypeEnum | None = None
    order: SortOrder | None = None


@dataclass
class TaskResponse:
    type: int
    body: str
    answer: str
    time_limit: int

    def get_data(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class TaskCompletedResponse:
    task_id: int
    user_id: int
    code: str
    completed_time: float

    def get_data(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class TaskRun:
    code: str
    time_limit: int
    answer: str


@dataclass
class TaskRunFullBodY(TaskRun):
    user_id: int
    task_id: int


@dataclass
class TaskRunRequest:
    code: str
    task_id: int


@dataclass
class TaskRunSubscriberRequest:
    uuid: str
    code: str
    answer: str
    time_limit: int


@dataclass
class TaskRunBrokerRequest:
    uuid: str
    code: str
    answer: str
    time_limit: int
