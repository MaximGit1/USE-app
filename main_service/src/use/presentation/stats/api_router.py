from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from use.application.stats.response import TaskProfileStatsResponse
from use.application.stats.service import StatsService

router = APIRouter(prefix="/stats", tags=["Stats"], route_class=DishkaRoute)


@router.get("/profile/{user_id}/")
async def get_profile_task_stats(
    user_id: int, stats_service: FromDishka[StatsService]
) -> list[TaskProfileStatsResponse]:
    return await stats_service.get_task_profile_data(user_id=user_id)
