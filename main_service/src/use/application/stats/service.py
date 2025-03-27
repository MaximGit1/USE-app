from use.application.stats.response import (
    TaskProfileStatsResponse, TaskAdminStatsResponse,
)
from use.application.task.protocols import TaskReadProtocol
from use.application.user.protocols import UserReadProtocol
from use.entities.task.enums import ALL_TASK_TYPES
from use.entities.user.value_objects import UserID


class StatsService:
    def __init__(self, task_read: TaskReadProtocol, user_read: UserReadProtocol) -> None:
        self._task_read = task_read
        self._user_read = user_read

    async def get_task_by_task_type_profile_data(
        self, user_id: int, task_type: int
    ) -> TaskProfileStatsResponse:
        user_completed_task_ids = (
            await self._task_read.get_completed_task_ids_by_user_id(
                user_id=UserID(user_id)
            )
        )

        counter = 0
        for task_id in user_completed_task_ids:
            task = await self._task_read.get_task_by_id(task_id=task_id)
            if task.type == task_type:
                counter += 1

        count_all_tasks = await self._task_read.get_count_tasks(
            task_type=task_type
        )

        return TaskProfileStatsResponse(
            task_type=task_type,
            completed_percent=round(counter / count_all_tasks * 100, 2)
            if count_all_tasks
            else 0,
            user_completed_tasks=counter,
            all_tasks=count_all_tasks,
        )

    async def get_task_profile_data(
        self, user_id: int
    ) -> list[TaskProfileStatsResponse]:
        return [
            await self.get_task_by_task_type_profile_data(
                user_id,
                task_type,
            )
            for task_type in ALL_TASK_TYPES
        ]

    async def get_tasks_admin_data(self) -> list[TaskAdminStatsResponse]:
        stats = []
        total_users = await self._user_read.get_users_count()
        for task_type in ALL_TASK_TYPES:
            completed_users = await self._task_read.get_count_completed_tasks_by_type(task_type)
            percent = round((completed_users / total_users) * 100, 2) if total_users else 0.0

            stats.append(
                TaskAdminStatsResponse(
                    task_type=task_type,
                    completed_percent=percent,
                )
            )
        return stats
