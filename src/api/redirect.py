from datetime import datetime, timezone
from typing import Annotated, Protocol

from fastapi import APIRouter, BackgroundTasks, Depends, Path, Request, status
from fastapi.responses import RedirectResponse

from src.api.dependencies import get_clicks_producer, get_link_service
from src.dto.clicks import LinkClickedDTO
from src.dto.links import LinksDTO
from src.producers.ports import IClicksProducer

router = APIRouter()


class ILinksServiceRedirect(Protocol):
    async def get_for_redirect(self, slug: str) -> LinksDTO: ...


@router.get("/{slug}")
async def get_for_redirect(
    slug: Annotated[str, Path()],
    links_service: Annotated[ILinksServiceRedirect, Depends(get_link_service)],
    request: Request,
    background_task: BackgroundTasks,
    clicks_producer: Annotated[IClicksProducer, Depends(get_clicks_producer)],
) -> RedirectResponse:
    link = await links_service.get_for_redirect(slug)

    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user_agent")
    referer = request.headers.get("referer")
    data = LinkClickedDTO(
        link_id=link.id,
        clicked_at=datetime.now(timezone.utc),
        ip_address=client_ip,
        user_agent=user_agent,
        referer=referer,
    )

    background_task.add_task(clicks_producer.send, data)

    headers = {"Cache-Control": "no-store, no-cache, must-revalidate"}

    return RedirectResponse(
        url=link.original_url, status_code=status.HTTP_302_FOUND, headers=headers
    )
