import logging
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Awaitable, Callable, Final

from redis.asyncio import Redis
from redis.exceptions import ConnectionError, TimeoutError

from src.dto.links import LinksDTO
from src.repositories.cache.links_json_serializer import LinksJsonSerializer

logger = logging.getLogger(__name__)


def handle_redis_error[**P, R](
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R | None]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return await func(*args, **kwargs)
        except (ConnectionError, TimeoutError):
            logger.warning("Redis is unavailable, args: %s", args, exc_info=True)
        return None

    return wrapper


class LinksCacheRepository:
    PREFIX: Final = "links:"
    DEFAULT_TTL = 24 * 3600

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def _calculate_ttl(self, expires_at: datetime | None) -> timedelta:
        if expires_at is None:
            return timedelta(seconds=self.DEFAULT_TTL)

        time_before_expires = expires_at - datetime.now(timezone.utc)

        if time_before_expires <= timedelta():
            return timedelta()

        return timedelta(
            seconds=(min(self.DEFAULT_TTL, time_before_expires.total_seconds()))
        )

    def _generate_key(self, slug: str) -> str:
        return self.PREFIX + slug

    @handle_redis_error
    async def set(self, link: LinksDTO) -> None:
        key = self._generate_key(link.slug)

        link_as_json = LinksJsonSerializer.to_json(link)

        ttl = self._calculate_ttl(link.expires_at)

        if ttl == timedelta():
            return

        await self.redis.set(
            name=key, value=link_as_json, ex=self._calculate_ttl(link.expires_at)
        )

    @handle_redis_error
    async def get(self, slug: str) -> LinksDTO | None:
        key = self._generate_key(slug)

        if link_as_json := await self.redis.get(key):
            return LinksJsonSerializer.from_json(link_as_json)

        return None

    @handle_redis_error
    async def delete(self, slug: str) -> None:
        key = self._generate_key(slug)

        await self.redis.delete(key)
