from src.consumers.clicks_consumer import ClicksConsumer
from src.consumers.ports import IClicksConsumer
from src.core.database import async_session
from src.repositories.database.unit_of_work import UnitOfWork
from src.services.clicks_service import ClicksService


def create_clicks_consumer() -> IClicksConsumer:
    uow = UnitOfWork(async_session)
    service = ClicksService(uow)

    return ClicksConsumer(service)
