from typing import Annotated

from fastapi import APIRouter, Depends, Path

from src.api.dependencies import get_clicks_service
from src.schemas.clicks import ClicksAnalyticsResponse
from src.services.ports import IClicksService

router = APIRouter()


@router.get("/links/{slug}/analytics", response_model=ClicksAnalyticsResponse)
async def get_metrics(
    slug: Annotated[str, Path()],
    clicks_service: Annotated[IClicksService, Depends(get_clicks_service)],
) -> ClicksAnalyticsResponse:
    return clicks_service.get_metrics(slug)
