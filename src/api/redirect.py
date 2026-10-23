from typing import Annotated, Protocol

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import RedirectResponse

from src.api.dependencies import get_link_service
from src.dto.links import LinksDTO

router = APIRouter()


class ILinksServiceRedirect(Protocol):
    async def get_for_redirect(self, slug: str) -> LinksDTO: ...


@router.get("/{slug}")
async def get_for_redirect(
    slug: Annotated[str, Path()],
    links_service: Annotated[ILinksServiceRedirect, Depends(get_link_service)],
) -> RedirectResponse:
    link = await links_service.get_for_redirect(slug)
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate"}

    return RedirectResponse(
        url=link.original_url, status_code=status.HTTP_302_FOUND, headers=headers
    )
