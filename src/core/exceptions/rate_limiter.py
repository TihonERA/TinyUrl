from src.core.exceptions.base import ApplicationError, DomainError


class RateLimitConcurrencyError(ApplicationError):
    def __init__(self, retry_after: int) -> None:
        self.retry_after = retry_after


class TooManyRequests(DomainError):
    def __init__(self, retry_after: int) -> None:
        super().__init__(
            f"Too many requests. Please try again after {retry_after} seconds"
        )
