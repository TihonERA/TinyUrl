from typing import Annotated

from fastapi import Depends

from src.core.cache import redis_client
from src.core.database import async_session
from src.repositories.cache.links_cache_repository import LinksCacheRepository
from src.repositories.cache.ports import ILinksCacheRepository, IRateLimiterRepository
from src.repositories.cache.rate_limiter_repository import RateLimiterRepository
from src.repositories.database.unit_of_work import IUnitOfWork, UnitOfWork
from src.services.links_service import IUnitOfWorkLinks, LinksService
from src.services.ports import ILinksService


def get_uow() -> IUnitOfWork:
    return UnitOfWork(async_session)


def get_links_cache_repo() -> ILinksCacheRepository:
    return LinksCacheRepository(redis_client)


def get_rate_limit_repo() -> IRateLimiterRepository:
    return RateLimiterRepository(redis_client)


def get_link_service(
    uow: Annotated[IUnitOfWorkLinks, Depends(get_uow)],
    links_cache_repo: Annotated[ILinksCacheRepository, Depends(get_links_cache_repo)],
) -> ILinksService:
    return LinksService(uow, links_cache_repo)
