from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.links import LinkNotFound
from src.dto.clicks import (
    ClicksSummaryMetrics,
    ClicksTimeBucket,
    ClicksUserAgentsMetrics,
)
from src.models.clicks import Clicks
from src.repositories.database.mappers.clicks_mapper import ClicksMapper


class ClicksRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        link_id: int,
        clicked_at: datetime,
        ip_address: str,
        user_agent: str | None,
        referer: str | None,
    ) -> None:
        click = Clicks(
            link_id=link_id,
            clicked_at=clicked_at,
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer,
        )

        try:
            self.session.add(click)
            await self.session.flush()
        except IntegrityError as err:
            raise LinkNotFound() from err

    async def get_clicks_metrics(self, link_id: int) -> ClicksSummaryMetrics:
        stmt = select(func.count(), func.count(func.distinct(Clicks.ip_address))).where(
            Clicks.link_id == link_id
        )

        result = await self.session.execute(stmt)
        total, unique = result.one()
        return ClicksMapper.to_clicks_metrics(total, unique)

    async def get_user_agents_metrics(
        self, link_id: int
    ) -> list[ClicksUserAgentsMetrics]:
        stmt = (
            select(Clicks.user_agent, func.count(Clicks.id))
            .where(Clicks.link_id == link_id)
            .group_by(Clicks.user_agent)
        )

        result = await self.session.execute(stmt)
        return ClicksMapper.to_list_clicks_user_agents_metrics(result.all())

    async def get_clicks_time_bucket(
        self, link_id: int, hours: int
    ) -> list[ClicksTimeBucket]:
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        time_bucket = func.date_trunc("hour", Clicks.clicked_at)

        stmt = (
            select(time_bucket, func.count(Clicks.id))
            .where(Clicks.link_id == link_id, Clicks.clicked_at > start_time)
            .group_by(time_bucket)
            .order_by(time_bucket.asc())
        )

        result = await self.session.execute(stmt)
        return ClicksMapper.to_list_clicks_time_bucket(result.all())
