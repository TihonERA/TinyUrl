from fastapi import FastAPI

from src.api import links, redirect
from src.api.handlers import domain_error_handler, unexpected_error_handler
from src.core.exceptions.base import DomainError

app = FastAPI()
app.include_router(links.router)
app.include_router(redirect.router)

app.exception_handler(Exception)(unexpected_error_handler)
app.exception_handler(DomainError)(domain_error_handler)
