from functools import wraps
from logging import getLogger
from typing import Awaitable, Callable

logger = getLogger(__name__)


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
