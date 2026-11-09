from pydantic import BaseModel, ConfigDict


class ClicksAnalyticsResponse(BaseModel):
    total: int
    unique: int
    browser: dict[str, int]
    os: dict[str, int]

    model_config = ConfigDict(from_attributes=True)
