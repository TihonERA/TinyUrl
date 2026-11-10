from datetime import datetime
from typing import Sequence

from sqlalchemy import Row

from src.dto.clicks import (
    ClicksSummaryMetrics,
    ClicksTimeBucket,
    ClicksUserAgentsMetrics,
)


class ClicksMapper:
    @staticmethod
    def to_clicks_metrics(total: int, unique: int) -> ClicksSummaryMetrics:
        return ClicksSummaryMetrics(total=total, unique=unique)

    @staticmethod
    def _to_clicks_user_agents_metrics(
        user_agent: str | None, count: int
    ) -> ClicksUserAgentsMetrics:
        return ClicksUserAgentsMetrics(user_agent=user_agent, count=count)

    @classmethod
    def to_list_clicks_user_agents_metrics(
        cls, data: Sequence[Row[str, int]]
    ) -> list[ClicksUserAgentsMetrics]:
        return [cls._to_clicks_user_agents_metrics(u, c) for u, c in data]

    @staticmethod
    def to_clicks_time_bucket(time: datetime, count: int) -> ClicksTimeBucket:
        return ClicksTimeBucket(time=time, count=count)

    @classmethod
    def to_list_clicks_time_bucket(
        cls, data: Sequence[Row[datetime, int]]
    ) -> list[ClicksTimeBucket]:
        return [cls.to_clicks_time_bucket(t, c) for t, c in data]
