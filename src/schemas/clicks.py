from pydantic import BaseModel, ConfigDict


class ClicksAnalyticsResponse(BaseModel):
    total_clicks: int
    unique_clicks: int
    browsers: dict[str, int]
    os: dict[str, int]

    model_config = ConfigDict(from_attributes=True)
