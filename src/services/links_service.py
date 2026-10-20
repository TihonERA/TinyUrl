import secrets
import string
from datetime import datetime
from typing import Protocol

from schemas.links import LinksCreateData
from src.core.exceptions.links import (
    LinkNotFound,
    SlugCreationError,
    SlugNotUniqueError,
)
from src.models.links import Links
from src.repositories.unit_of_work import IUnitOfWork


class ILinksRepository(Protocol):
    async def create(
        self, slug: str, original_url: str, expires_at: datetime, is_active: bool = True
    ) -> Links: ...
    async def get(self, slug: str) -> Links | None: ...
    async def delete(self, id: int) -> None: ...


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

    async def create(self, link_create_data: LinksCreateData) -> Links:
        MAX_RETRIES = 3

        for _ in range(MAX_RETRIES):
            try:
                async with self.uow:
                    link = await self.uow.links_repo.create(
                        slug=self._generate_base62(),
                        original_url=link_create_data.original_url,
                        expires_at=link_create_data.expires_at,
                        is_active=link_create_data.is_active,
                    )

                    await self.uow.commit()

                    return link
            except SlugNotUniqueError:
                pass

        raise SlugCreationError()

    async def get(self, slug: str) -> Links:
        async with self.uow:
            link = await self.uow.links_repo.get(slug)

            if link is None:
                raise LinkNotFound()

            return link

    async def delete(self, id: int) -> None:
        async with self.uow:
            await self.uow.links_repo.delete(id)
            await self.uow.commit()
