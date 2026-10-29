from datetime import datetime, timezone
from functools import partial
from typing import Final, cast
from uuid import uuid4

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline


class RateLimiterRepository:
    WINDOW_LENGTH: Final = 60
    PREFIX: Final = "rate_limiter"

    def __init__(self, rate_limit: int, redis: Redis) -> None:
        self.rate_limit = rate_limit
        self.redis = redis

    def _formate_key(self, endpoint: str, ip: str) -> str:
        return ":".join([self.PREFIX, endpoint, ip])

    async def logic(self, pipe: Pipeline, key: str) -> bool:
        current_timestamp = datetime.now(timezone.utc).timestamp()
        last_window_timestamp = current_timestamp - self.WINDOW_LENGTH

        request_count = await pipe.zcount(
            name=key, min=last_window_timestamp, max="+inf"
        )

        pipe.multi()

        pipe.zremrangebyscore(key, min="-inf", max=last_window_timestamp)

        if request_count >= self.rate_limit:
            return False

        pipe.zadd(
            name=key,
            mapping={f"{current_timestamp}:{uuid4().hex}": current_timestamp},
        )

        next_window_timestamp = int(current_timestamp + 61)
        pipe.expireat(name=key, when=next_window_timestamp)

        await pipe.execute()
        return True

    async def placeholder(self, endpoint: str, ip: str) -> bool:
        key = self._formate_key(endpoint, ip)

        logic = partial(self.logic, key=key)

        result = cast(bool, await self.redis.transaction(logic, key))
        return result
