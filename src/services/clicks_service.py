from typing import Protocol

from src.dto.clicks import LinkClickedDTO
from src.repositories.database.ports import IClicksRepository
from src.repositories.database.unit_of_work import UnitOfWork


class IUnitOfWorkClicks(Protocol):
    clicks_repo: IClicksRepository


class ClicksService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create(self, data: LinkClickedDTO) -> None:
        async with self.uow:
            await self.uow.clicks_repo.create(
                link_id=data.link_id,
                ip_address=data.ip_address,
                user_agent=data.user_agent,
                referer=data.referer,
            )

            await self.uow.commit()
