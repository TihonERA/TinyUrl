from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimiterResult:
    status: bool
    retry_after: int | None
