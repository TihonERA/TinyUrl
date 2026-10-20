from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.links import SlugNotUniqueError
from src.models.links import Links


class LinksRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self, slug: str, original_url: str, expires_at: datetime, is_active: bool = True
    ) -> Links:
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

        return link

    async def get(self, slug: str) -> Links | None:
        stmt = select(Links).where(Links.slug == slug)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> None:
        stmt = delete(Links).where(Links.id == id)

        await self.session.execute(stmt)
