from datetime import datetime

from sqlalchemy import Result, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.links import SlugNotUniqueError
from src.dto.links import LinksDTO
from src.models.links import Links
from src.repositories.links_mapper import LinksMapper


class LinksRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        slug: str,
        original_url: str,
        expires_at: datetime | None,
        is_active: bool = True,
    ) -> LinksDTO:
        link = Links(
            slug=slug,
            original_url=original_url,
            is_active=is_active,
            expires_at=expires_at,
        )

        try:
            self.session.add(link)
            await self.session.flush()
        except IntegrityError as err:
            raise SlugNotUniqueError() from err

        return LinksMapper.to_dto(link)

    @staticmethod
    def _result_to_dto_or_none(result: Result[Links]) -> LinksDTO | None:
        link = result.scalar_one_or_none()

        if link is None:
            return None

        return LinksMapper.to_dto(link)

    async def get(self, slug: str) -> LinksDTO | None:
        stmt = select(Links).where(Links.slug == slug)

        result = await self.session.execute(stmt)
        return self._result_to_dto_or_none(result)

    async def deactivate(self, slug: str) -> LinksDTO | None:
        stmt = (
            update(Links)
            .where(Links.slug == slug)
            .values(is_active=False)
            .returning(Links)
        )

        result = await self.session.execute(stmt)
        return self._result_to_dto_or_none(result)

    async def delete(self, slug: str) -> None:
        stmt = delete(Links).where(Links.slug == slug)

        await self.session.execute(stmt)
