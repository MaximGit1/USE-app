
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from use.application.common.request.models import PaginationParams, SortOrder
from use.application.user.request.models import (
    SearchFilters,
    SearchFilterTypes,
)
from use.application.user.response.models import (
    UserFullBodyResponse,
)
from use.application.user.service import UserService
from use.presentation.user.schemes import UserRoleScheme

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get("/")
async def get_all(
    user_service: FromDishka[UserService],
    offset: int = 0,
    limit: int = 10,
    order_by: SearchFilterTypes | None = None,
    sortorder: SortOrder | None = None,
) -> list[UserFullBodyResponse]:
    return await user_service.get_all(
        pagination=PaginationParams(
            offset=offset,
            limit=limit,
        ),
        filters=SearchFilters(
            order_by=order_by,
            order=sortorder,
        ),
    )


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    return await user_service.get_by_id(user_id=user_id)


@router.get("/username/{username}")
async def get_user_by_username(
    username: str, user_service: FromDishka[UserService]
) -> UserFullBodyResponse:
    return await user_service.get_by_username(username=username)


@router.patch("/{user_id}/update/role")
async def update_role(
    user_id: int,
    role: UserRoleScheme,
    user_service: FromDishka[UserService],
) -> None:
    await user_service.change_role(
        user_id=user_id,
        role=role.get_role(),
    )


@router.patch("/{user_id}/update/status/")
async def update_user_status(
    user_id: int,
    *,
    is_active: bool,
    user_service: FromDishka[UserService],
) -> None:
    await user_service.change_status(
        user_id=user_id,
        is_active=is_active,
    )
