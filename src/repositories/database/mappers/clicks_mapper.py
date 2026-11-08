from typing import Sequence

from sqlalchemy import Row

from src.dto.clicks import (
    ClicksSummaryMetrics,
    ClicksUserAgentsMetrics,
)


class ClicksMapper:
    @staticmethod
    def to_clicks_metrics(total: int, unique: int) -> ClicksSummaryMetrics:
        return ClicksSummaryMetrics(total=total, unique=unique)

    @staticmethod
    def _to_clicks_user_agents_metrics(
        user_agent: str, count: int
    ) -> ClicksUserAgentsMetrics:
        return ClicksUserAgentsMetrics(user_agent=user_agent, count=count)

    @classmethod
    def to_list_clicks_user_agents_metrics(
        cls, data: Sequence[Row[str, int]]
    ) -> list[ClicksUserAgentsMetrics]:
        return [cls._to_clicks_user_agents_metrics(u, c) for u, c in data]
