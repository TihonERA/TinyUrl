from datetime import datetime
from typing import Protocol

from src.dto.clicks import (
    ClicksSummaryMetrics,
    ClicksTimeBucket,
    ClicksUserAgentsMetrics,
)
from src.dto.links import LinksDTO


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


class IClicksRepository(Protocol):
    async def create(
        self,
        link_id: int,
        clicked_at: datetime,
        ip_address: str,
        user_agent: str | None,
        referer: str | None,
    ) -> None: ...
    async def get_clicks_metrics(self, link_id: int) -> ClicksSummaryMetrics: ...
    async def get_user_agents_metrics(
        self, link_id: int
    ) -> list[ClicksUserAgentsMetrics]: ...
    async def get_clicks_time_bucket(
        self, link_id: int, hours: int
    ) -> list[ClicksTimeBucket]: ...
