from typing import Annotated

from fastapi import Depends

from src.core.database import async_session
from src.repositories.unit_of_work import IUnitOfWork, UnitOfWork
from src.services.links_service import IUnitOfWorkLinks, LinksService
from src.services.ports import ILinksService


def get_uow() -> IUnitOfWork:
    return UnitOfWork(async_session)


def get_link_service(
    uow: Annotated[IUnitOfWorkLinks, Depends(get_uow)],
) -> ILinksService:
    return LinksService(uow)
