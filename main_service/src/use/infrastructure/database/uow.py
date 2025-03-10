from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from use.application.common.protocols.uow import UoWProtocol

if TYPE_CHECKING:
    import types

    from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUoW(UoWProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def flush(self) -> None:
        await self._session.flush()

    async def refresh(self, instance: Any) -> None:
        await self._session.refresh(instance)

    async def rollback(self) -> None:
        await self._session.rollback()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self._session.close()
