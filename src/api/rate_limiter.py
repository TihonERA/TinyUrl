from typing import Annotated

from fastapi import Depends, Request

from src.api.dependencies import get_rate_limit_repo
from src.core.exceptions.rate_limiter import TooManyRequests
from src.repositories.cache.ports import IRateLimiterRepository


class RateLimiter:
    def __init__(self, rate_limit: int = 10, window: int = 60) -> None:
        self.rate_limit = rate_limit
        self.window = window

    async def __call__(
        self,
        request: Request,
        rate_limit_repo: Annotated[
            IRateLimiterRepository, Depends(get_rate_limit_repo)
        ],
    ) -> None:
        endpoint = request.url.path
        ip = request.client.host if request.client is not None else "unknown"

        retry_after = await rate_limit_repo.is_allowed(
            endpoint=endpoint, ip=ip, rate_limit=self.rate_limit, window=self.window
        )

        if retry_after is not None:
            raise TooManyRequests(retry_after)
