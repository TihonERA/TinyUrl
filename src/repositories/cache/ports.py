from typing import Protocol

from src.dto.clicks import ClicksMetrics
from src.dto.links import LinksDTO


class ILinksCacheRepository(Protocol):
    async def set(self, link: LinksDTO) -> None: ...
    async def get(self, slug: str) -> LinksDTO | None: ...
    async def delete(self, slug: str) -> None: ...


class IClicksCacheRepository(Protocol):
    async def get(self, slug: str) -> ClicksMetrics | None: ...
    async def set(self, slug: str, metrics: ClicksMetrics) -> None: ...


class IRateLimiterRepository(Protocol):
    async def is_allowed(
        self, endpoint: str, ip: str, rate_limit: int, window: int
    ) -> int | None: ...
