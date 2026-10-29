from datetime import datetime, timezone
from functools import partial
from math import ceil
from typing import Final, cast
from uuid import uuid4

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

from src.repositories.cache.error_handler import handle_redis_error


class RateLimiterRepository:
    PREFIX: Final = "rate_limiter"

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def _formate_key(self, endpoint: str, ip: str) -> str:
        return ":".join([self.PREFIX, endpoint, ip])

    async def _is_allowed_logic(
        self, pipe: Pipeline, key: str, rate_limit: int, window: int
    ) -> int | None:
        current_timestamp = datetime.now(timezone.utc).timestamp()
        last_window_timestamp = current_timestamp - window

        request_count = await pipe.zcount(
            name=key, min=last_window_timestamp, max="+inf"
        )

        if request_count >= rate_limit:
            oldest_request = await pipe.zrangebyscore(
                name=key,
                min=last_window_timestamp,
                max="+inf",
                start=0,
                num=1,
                withscores=True,
            )

            if not oldest_request:
                return window

            _, timestamp_score = oldest_request[0]
            timestamp_score = float(timestamp_score)

            retry_after = max(1, ceil(timestamp_score + window - current_timestamp))

            return retry_after

        pipe.multi()

        pipe.zremrangebyscore(key, min="-inf", max=last_window_timestamp)

        pipe.zadd(
            name=key,
            mapping={f"{current_timestamp}:{uuid4().hex}": current_timestamp},
        )

        pipe.expire(name=key, time=window)

    @handle_redis_error
    async def is_allowed(
        self, endpoint: str, ip: str, rate_limit: int, window: int = 60
    ) -> int | None:
        key = self._formate_key(endpoint, ip)

        logic = partial(
            self._is_allowed_logic, key=key, rate_limit=rate_limit, window=window
        )

        result = cast(
            int | None,
            await self.redis.transaction(logic, key, value_from_callable=True),
        )

        return result
