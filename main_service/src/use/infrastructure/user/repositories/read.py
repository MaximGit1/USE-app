from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, asc, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from use.application.common.request.models import (
    PaginationParams,
    SortOrder,
)
from use.application.user.protocols import UserReadProtocol
from use.application.user.request.models import (
    SearchFilters,
    SearchFilterTypes,
)
from use.entities.user.enums import RoleEnum
from use.entities.user.models import User
from use.entities.user.value_objects import (
    HashedPassword,
    UserID,
    Username,
)
from use.infrastructure.database.models import users_table


class UserReadRepository(UserReadProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UserID) -> User | None:
        stmt = select(users_table).where(users_table.c.id == user_id.value)
        result = (await self._session.execute(stmt)).one_or_none()

        if result is None:
            return None

        return self._load_user(result)

    async def get_by_username(self, username: Username) -> User | None:
        stmt = select(users_table).where(
            users_table.c.username == username.value
        )
        result = (await self._session.execute(stmt)).one_or_none()

        if result is None:
            return None

        return self._load_user(result)

    async def get_all(
        self, pagination: PaginationParams, filters: SearchFilters
    ) -> list[User]:
        stmt = (
            select(users_table)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )

        if filters.order_by == SearchFilterTypes.USERNAME:
            order_by_value = users_table.c.username
        else:
            order_by_value = users_table.c.id

        if filters.order == SortOrder.ASC:
            stmt = stmt.order_by(asc(order_by_value))
        elif filters.order == SortOrder.DESC:
            stmt = stmt.order_by(desc(order_by_value))

        result = await self._session.execute(stmt)

        return self._load_users(result.all())

    async def get_users_count(self) -> int:
        stmt = select(func.count()).select_from(users_table)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    def _load_user(self, row: Row[Any]) -> User:
        return User(
            id=UserID(row.id),
            username=Username(row.username),
            hashed_password=HashedPassword(row.hashed_password),
            role=self._convert_role(row.role),
            is_active=row.is_active,
        )

    @staticmethod
    def _convert_role(role: str) -> RoleEnum:
        if role == RoleEnum.USER:
            return RoleEnum.USER
        if role == RoleEnum.ADMIN:
            return RoleEnum.ADMIN
        if role == RoleEnum.MODERATOR:
            return RoleEnum.MODERATOR
        return RoleEnum.GUEST

    def _load_users(self, rows: Sequence[Row[Any]]) -> list[User]:
        return [self._load_user(row) for row in rows]
