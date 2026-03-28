from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl = Field(..., description="The original URL to shorten.")
    expires_at: datetime | None = Field(
        default=None,
        description="Optional expiration time for the shortened URL.",
    )


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    clicks: int
    created_at: datetime | None
    expires_at: datetime | None
