from collections import defaultdict
from typing import Protocol

from user_agents import parse

from src.core.exceptions.links import LinkNotFound
from src.dto.clicks import (
    ClicksMetrics,
    ClicksSummaryMetrics,
    ClicksUserAgentsMetrics,
    LinkClickedDTO,
)
from src.repositories.database.ports import IClicksRepository, ILinksRepository
from src.repositories.database.unit_of_work import IUnitOfWork


class IUnitOfWorkClicks(IUnitOfWork, Protocol):
    links_repo: ILinksRepository
    clicks_repo: IClicksRepository


class ClicksService:
    def __init__(self, uow: IUnitOfWorkClicks) -> None:
        self.uow = uow

    async def create(self, data: LinkClickedDTO) -> None:
        async with self.uow:
            await self.uow.clicks_repo.create(
                link_id=data.link_id,
                clicked_at=data.clicked_at,
                ip_address=data.ip_address,
                user_agent=data.user_agent,
                referer=data.referer,
            )

            await self.uow.commit()

    @staticmethod
    def _calculate_clicks_metrics(
        summary_metrics: ClicksSummaryMetrics,
        user_agents_metrics: list[ClicksUserAgentsMetrics],
    ) -> ClicksMetrics:
        browser_data = defaultdict(int)
        os_data = defaultdict(int)

        for user_agent_data in user_agents_metrics:
            if user_agent_data.user_agent is None:
                browser_data["Unknown"] += user_agent_data.count
                os_data["Unknown"] += user_agent_data.count
                continue

            parsed_user_agent = parse(user_agent_data.user_agent)

            browser_data[parsed_user_agent.browser.family] += user_agent_data.count
            os_data[parsed_user_agent.os.family] += user_agent_data.count

        return ClicksMetrics(
            total_clicks=summary_metrics.total,
            unique_clicks=summary_metrics.unique,
            browsers=browser_data,
            os=os_data,
        )

    async def get_metrics(self, slug: str) -> ClicksMetrics:
        async with self.uow:
            if (link := await self.uow.links_repo.get(slug)) is None:
                raise LinkNotFound()

            summary_metrics = await self.uow.clicks_repo.get_clicks_metrics(link.id)
            user_agents_metrics = await self.uow.clicks_repo.get_user_agents_metrics(
                link.id
            )

        return self._calculate_clicks_metrics(summary_metrics, user_agents_metrics)
