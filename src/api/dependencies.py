from typing import Annotated

from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool
from fastapi import Depends

from src.core.broker import broker
from src.core.cache import redis_client
from src.core.database import async_session
from src.producers.clicks_producer import ClicksProducer
from src.producers.ports import IClicksProducer
from src.repositories.cache.links_cache_repository import LinksCacheRepository
from src.repositories.cache.ports import ILinksCacheRepository, IRateLimiterRepository
from src.repositories.cache.rate_limiter_repository import RateLimiterRepository
from src.repositories.database.unit_of_work import IUnitOfWork, UnitOfWork
from src.services.links_service import IUnitOfWorkLinks, LinksService
from src.services.ports import ILinksService


def get_uow() -> IUnitOfWork:
    return UnitOfWork(async_session)


async def get_rmq_channel_pool() -> Pool[AbstractChannel]:
    if broker.channel_pool is None:
        raise RuntimeError("Connection pool is not initialized")

    return broker.channel_pool


def get_links_cache_repo() -> ILinksCacheRepository:
    return LinksCacheRepository(redis_client)


def get_rate_limit_repo() -> IRateLimiterRepository:
    return RateLimiterRepository(redis_client)


def get_clicks_producer(
    channel_pool: Annotated[Pool[AbstractChannel], Depends(get_rmq_channel_pool)],
) -> IClicksProducer:
    return ClicksProducer(channel_pool)


def get_link_service(
    uow: Annotated[IUnitOfWorkLinks, Depends(get_uow)],
    links_cache_repo: Annotated[ILinksCacheRepository, Depends(get_links_cache_repo)],
) -> ILinksService:
    return LinksService(uow, links_cache_repo)
