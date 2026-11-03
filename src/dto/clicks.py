from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LinkClickedDTO:
    link_id: int
    clicked_at: datetime
    ip_address: str | None
    user_agent: str | None
    referer: str | None
