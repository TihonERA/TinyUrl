from typing import Final

from redis.asyncio import Redis

from src.dto.clicks import ClicksMetrics
from src.repositories.cache.error_handler import handle_redis_error
from src.repositories.cache.serializers.clicks_json_serializer import (
    ClicksJsonSerializer,
)


class ClicksCacheRepository:
    PREFIX: Final = "analytics:"
    DEFAULT_TTL: Final = 60

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def _generate_key(self, slug: str) -> str:
        return self.PREFIX + slug

    @handle_redis_error
    async def get(self, slug: str) -> ClicksMetrics | None:
        key = self._generate_key(slug)

        if clicks_metrics_as_json := await self.redis.get(key):
            return ClicksJsonSerializer.from_json(clicks_metrics_as_json)

        return None

    @handle_redis_error
    async def set(self, slug: str, metrics: ClicksMetrics) -> None:
        key = self._generate_key(slug)

        metrics_as_json = ClicksJsonSerializer.to_json(metrics)

        await self.redis.set(name=key, value=metrics_as_json, ex=self.DEFAULT_TTL)
