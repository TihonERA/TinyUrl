from datetime import datetime

from pydantic import BaseModel


class LinksCreateData(BaseModel):
    original_url: str
    is_active: bool = True
    expires_at: datetime
