from src.core.database import async_session
from src.repositories.unit_of_work import IUnitOfWork, UnitOfWork


def get_uow() -> IUnitOfWork:
    return UnitOfWork(async_session)
