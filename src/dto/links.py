from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LinksDTO:
    id: int
    slug: str
    original_url: str
    is_active: bool
    created_at: datetime
    expires_at: datetime | None
