from datetime import datetime
from typing import Protocol, Sequence

from src.dto.links import LinksDTO
from src.models.clicks import Clicks


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
    ) -> Clicks: ...
    async def get_multiple(self, link_id: int, page: int) -> Sequence[Clicks]: ...
