from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClicksTimeBucketResponse(BaseModel):
    time: datetime
    count: int

    model_config = ConfigDict(from_attributes=True)


class ClicksAnalyticsResponse(BaseModel):
    total_clicks: int
    unique_clicks: int
    browsers: dict[str, int]
    os: dict[str, int]
    clicks_by_hour: list[ClicksTimeBucketResponse]

    model_config = ConfigDict(from_attributes=True)
