from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from use.application.stats.response import TaskProfileStatsResponse, TaskAdminStatsResponse
from use.application.stats.service import StatsService

router = APIRouter(prefix="/stats", tags=["Stats"], route_class=DishkaRoute)


@router.get("/profile/{user_id}/")
async def get_profile_task_stats(
    user_id: int, stats_service: FromDishka[StatsService]
) -> list[TaskProfileStatsResponse]:
    return await stats_service.get_task_profile_data(user_id=user_id)

@router.get("/admin/")
async def get_admin_task_stats(
    stats_service: FromDishka[StatsService]
) -> list[TaskAdminStatsResponse]:
    return await stats_service.get_tasks_admin_data()
