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
    user_agent: str
    count: int


@dataclass(frozen=True)
class ListClicksUserAgentsMetrics:
    list: list[ClicksUserAgentsMetrics]


@dataclass(frozen=True)
class ClicksMetrics:
    total: int
    count: int
    browser: dict[str, int]
    os: dict[str, int]
