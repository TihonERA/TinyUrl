import secrets
import string
from datetime import datetime, timezone
from typing import Protocol

from src.core.exceptions.links import (
    LinkExpiredError,
    LinkNotFound,
    SlugCreationError,
    SlugNotUniqueError,
)
from src.dto.links import LinksDTO
from src.repositories.unit_of_work import IUnitOfWork
from src.schemas.links import LinksCreateData


class ILinksRepository(Protocol):
    async def create(
        self,
        slug: str,
        original_url: str,
        expires_at: datetime | None,
        is_active: bool = True,
    ) -> LinksDTO: ...
    async def get(self, slug: str) -> LinksDTO | None: ...
    async def deactivate(self, slug: str) -> LinksDTO | None: ...
    async def delete(self, slug: str) -> None: ...


class IUnitOfWorkLinks(IUnitOfWork, Protocol):
    links_repo: ILinksRepository


class LinksService:
    BASE62_SYMBOLS = string.ascii_letters + string.digits
    BASE62_LENGTH = 8

    def __init__(self, uow: IUnitOfWorkLinks) -> None:
        self.uow = uow

    @classmethod
    def _generate_base62(cls) -> str:
        return "".join(
            secrets.choice(cls.BASE62_SYMBOLS) for _ in range(cls.BASE62_LENGTH)
        )

    async def create(self, link_create_data: LinksCreateData) -> LinksDTO:
        MAX_RETRIES = 3

        for _ in range(MAX_RETRIES):
            try:
                async with self.uow:
                    link = await self.uow.links_repo.create(
                        slug=self._generate_base62(),
                        original_url=str(link_create_data.original_url),
                        expires_at=link_create_data.expires_at,
                        is_active=link_create_data.is_active,
                    )

                    await self.uow.commit()

                    return link
            except SlugNotUniqueError:
                pass

        raise SlugCreationError()

    async def get(self, slug: str) -> LinksDTO:
        async with self.uow:
            link = await self.uow.links_repo.get(slug)

            if link is None:
                raise LinkNotFound()

            if not link.is_active:
                raise LinkNotFound()

            current_time = datetime.now(timezone.utc)

            if link.expires_at is not None and current_time > link.expires_at:
                raise LinkExpiredError()

            return link

    async def deactivate(self, slug: str) -> LinksDTO:
        async with self.uow:
            link = await self.uow.links_repo.deactivate(slug)

            if link is None:
                raise LinkNotFound()

            await self.uow.commit()

            return link

    async def delete(self, slug: str) -> None:
        async with self.uow:
            await self.uow.links_repo.delete(slug)
            await self.uow.commit()
