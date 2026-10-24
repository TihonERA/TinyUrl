from types import TracebackType
from typing import Protocol, Self, Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.repositories.database.clicks_repository import ClicksRepository
from src.repositories.database.links_repository import LinksRepository


class IUnitOfWork(Protocol):
    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    async def rollback(self) -> None: ...
    async def commit(self) -> None: ...


class UnitOfWork:
    def __init__(self, async_sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self.async_sessionmaker = async_sessionmaker

    async def __aenter__(self) -> Self:
        self.session = self.async_sessionmaker()

        self.links_repo = LinksRepository(self.session)
        self.clicks_repo = ClicksRepository(self.session)

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            await self.session.close()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()
