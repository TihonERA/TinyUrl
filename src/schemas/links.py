from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class LinksCreateData(BaseModel):
    original_url: HttpUrl
    is_active: bool = True
    expires_at: datetime | None = None


class LinksResponse(BaseModel):
    id: int
    slug: str
    original_url: str
    is_active: bool
    created_at: datetime
    expires_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
