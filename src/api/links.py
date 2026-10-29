from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status

from src.api.dependencies import get_link_service
from src.api.rate_limiter import RateLimiter
from src.schemas.links import LinksCreateData, LinksResponse
from src.services.ports import ILinksService

router = APIRouter(prefix="/links")


@router.get("/{slug}", response_model=LinksResponse)
async def get(
    slug: Annotated[str, Path()],
    links_service: Annotated[ILinksService, Depends(get_link_service)],
):
    return await links_service.get(slug)


@router.post(
    "",
    response_model=LinksResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter())],
)
async def create(
    link_create_data: Annotated[LinksCreateData, Body()],
    links_service: Annotated[ILinksService, Depends(get_link_service)],
):
    return await links_service.create(link_create_data)


@router.patch("/{slug}/deactivate", response_model=LinksResponse)
async def deactivate(
    slug: Annotated[str, Path()],
    links_service: Annotated[ILinksService, Depends(get_link_service)],
):
    return await links_service.deactivate(slug)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    slug: Annotated[str, Path()],
    links_service: Annotated[ILinksService, Depends(get_link_service)],
) -> None:
    return await links_service.delete(slug)
