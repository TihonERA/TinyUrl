from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.links import LinkNotFound
from src.models.clicks import Clicks


class ClicksRepository:
    PAGE_LENGTH = 10

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self, link_id: int, ip_address: str, user_agent: str | None, referer: str | None
    ) -> Clicks:
        click = Clicks(
            link_id=link_id,
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer,
        )

        try:
            self.session.add(click)
            await self.session.flush()
        except IntegrityError as err:
            raise LinkNotFound() from err

        return click

    async def get_multiple(self, link_id: int, page: int) -> Sequence[Clicks]:
        page_offset = page * self.PAGE_LENGTH

        stmt = (
            select(Clicks)
            .where(Clicks.link_id == link_id)
            .offset(page_offset)
            .limit(self.PAGE_LENGTH)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
