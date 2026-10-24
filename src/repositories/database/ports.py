from datetime import datetime
from typing import Protocol

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
