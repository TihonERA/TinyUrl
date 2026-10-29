from datetime import datetime, timezone
from functools import partial
from math import ceil
from typing import Final, cast
from uuid import uuid4

from redis.asyncio import Redis, WatchError
from redis.asyncio.client import Pipeline

from src.core.exceptions.rate_limiter import RateLimitCheckError
from src.dto.rate_limiter import RateLimiterResult


class RateLimiterRepository:
    WINDOW_LENGTH: Final = 60
    PREFIX: Final = "rate_limiter"

    def __init__(self, rate_limit: int, redis: Redis) -> None:
        self.rate_limit = rate_limit
        self.redis = redis

    def _formate_key(self, endpoint: str, ip: str) -> str:
        return ":".join([self.PREFIX, endpoint, ip])

    async def logic(self, pipe: Pipeline, key: str) -> RateLimiterResult:
        current_timestamp = datetime.now(timezone.utc).timestamp()
        last_window_timestamp = current_timestamp - self.WINDOW_LENGTH

        request_count = await pipe.zcount(
            name=key, min=last_window_timestamp, max="+inf"
        )

        if request_count >= self.rate_limit:
            oldest_request = await pipe.zrangebyscore(
                name=key,
                min=last_window_timestamp,
                max="+inf",
                start=0,
                num=1,
                withscores=True,
            )

            if not oldest_request:
                return RateLimiterResult(status=False, retry_after=self.WINDOW_LENGTH)

            _, timestamp_score = oldest_request[0]
            timestamp_score = float(timestamp_score)

            retry_after = ceil(timestamp_score + self.WINDOW_LENGTH - current_timestamp)

            return RateLimiterResult(status=False, retry_after=retry_after)

        pipe.multi()

        pipe.zremrangebyscore(key, min="-inf", max=last_window_timestamp)

        pipe.zadd(
            name=key,
            mapping={f"{current_timestamp}:{uuid4().hex}": current_timestamp},
        )

        pipe.expire(name=key, time=self.WINDOW_LENGTH)

        await pipe.execute()
        return RateLimiterResult(status=True, retry_after=None)

    async def placeholder(self, endpoint: str, ip: str) -> RateLimiterResult:
        key = self._formate_key(endpoint, ip)

        logic = partial(self.logic, key=key)

        try:
            result = cast(RateLimiterResult, await self.redis.transaction(logic, key))
        except WatchError as err:
            raise RateLimitCheckError() from err

        return result
