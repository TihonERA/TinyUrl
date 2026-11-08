from collections import defaultdict
from typing import Protocol

from user_agents import parse

from src.dto.clicks import ClicksMetrics, LinkClickedDTO
from src.repositories.database.ports import IClicksRepository
from src.repositories.database.unit_of_work import IUnitOfWork


class IUnitOfWorkClicks(IUnitOfWork, Protocol):
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

    async def get_metrics(self, link_id: int):
        async with self.uow:
            clicks_summary_metrics = await self.uow.clicks_repo.get_clicks_metrics(
                link_id
            )
            user_agents = await self.uow.clicks_repo.get_user_agents_metricss(link_id)
            browser_data = defaultdict(int)
            os_data = defaultdict(int)

            for user_agent_data in user_agents:
                if user_agent_data is None:
                    browser_data["Unknown"] += user_agent_data.count
                    os_data["Unknown"] += user_agent_data.count
                    continue

                parsed_user_agent = parse(user_agent_data.user_agent)

                browser_data[parsed_user_agent.browser.family] += user_agent_data.count
                os_data[parsed_user_agent.os.family] += user_agent_data.count

            return ClicksMetrics(
                total=clicks_summary_metrics.total,
                unique=clicks_summary_metrics.unique,
                browser=browser_data,
                os=os_data,
            )
