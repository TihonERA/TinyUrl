from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LinkClickedDTO:
    link_id: int
    clicked_at: datetime
    ip_address: str
    user_agent: str | None
    referer: str | None


@dataclass(frozen=True)
class ClicksSummaryMetrics:
    total: int
    unique: int


@dataclass(frozen=True)
class ClicksUserAgentsMetrics:
    user_agent: str | None
    count: int


@dataclass(frozen=True)
class ClicksTimeBucket:
    time: datetime
    count: int


@dataclass(frozen=True)
class ClicksMetrics:
    total_clicks: int
    unique_clicks: int
    browsers: dict[str, int]
    os: dict[str, int]
    clicks_by_hour: list[ClicksTimeBucket]
