from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import get_settings

async_engine = create_async_engine(
    url=str(get_settings().POSTGRES_URL),
    pool_size=10,
    max_overflow=20,
    pool_timeout=10,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
