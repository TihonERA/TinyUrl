from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api import links, redirect
from src.api.handlers import (
    domain_error_handler,
    too_many_requests_error_handler,
    unexpected_error_handler,
)
from src.core.broker import broker
from src.core.exceptions.base import DomainError
from src.core.exceptions.rate_limiter import TooManyRequests


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await broker.initialize()
    await broker.initialize_clicks_topology()

    yield

    await broker.close()


app = FastAPI(lifespan=lifespan)
app.include_router(links.router)
app.include_router(redirect.router)

app.exception_handler(Exception)(unexpected_error_handler)
app.exception_handler(DomainError)(domain_error_handler)
app.exception_handler(TooManyRequests)(too_many_requests_error_handler)
