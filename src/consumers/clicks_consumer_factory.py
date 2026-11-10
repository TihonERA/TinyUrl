from src.consumers.clicks_consumer import ClicksConsumer
from src.consumers.ports import IClicksConsumer
from src.core.cache import redis_client
from src.core.database import async_session
from src.repositories.cache.clicks_cache_repository import ClicksCacheRepository
from src.repositories.database.unit_of_work import UnitOfWork
from src.services.clicks_service import ClicksService


def create_clicks_consumer() -> IClicksConsumer:
    uow = UnitOfWork(async_session)
    cache_repo = ClicksCacheRepository(redis_client)
    service = ClicksService(uow, cache_repo)

    return ClicksConsumer(service)
