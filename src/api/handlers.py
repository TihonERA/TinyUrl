from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.core.exceptions.base import DomainError
from src.core.exceptions.links import (
    LinkExpiredError,
    LinkNotFound,
    SlugCreationError,
)
from src.core.exceptions.rate_limiter import TooManyRequests
from src.schemas.errors import ErrorResponse

logger = getLogger(__name__)

ERROR_MAP: dict[type[DomainError], tuple[int, str]] = {
    LinkNotFound: (status.HTTP_404_NOT_FOUND, "LINK_NOT_FOUND"),
    SlugCreationError: (status.HTTP_500_INTERNAL_SERVER_ERROR, "SLUG_CREATION"),
    LinkExpiredError: (status.HTTP_410_GONE, "LINK_EXPIRED"),
    TooManyRequests: (status.HTTP_429_TOO_MANY_REQUESTS, "TOO_MANY_REQUESTS"),
}

DEFAULT_ERROR = (status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR")


def _log_unexpected_error(exc: Exception) -> None:
    logger.exception(f"Unhandled Error: {str(exc)}")


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    status_code, code = ERROR_MAP.get(type(exc), DEFAULT_ERROR)

    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("Domain internal server error [%s]: %s", code, exc, exc_info=True)

    payload = ErrorResponse(code=code, message=str(exc))
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    status_code, code = DEFAULT_ERROR

    _log_unexpected_error(exc)

    payload = ErrorResponse(code=code, message="Internal Server Error")
    return JSONResponse(status_code=status_code, content=payload.model_dump())
