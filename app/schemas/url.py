from datetime import datetime, timezone

from pydantic import BaseModel, Field, HttpUrl, root_validator, validator


class URLCreate(BaseModel):
    original_url: HttpUrl = Field(..., description="The original URL to shorten.")
    expiry_days: int | None = Field(
        default=None,
        description="Optional number of days before the shortened URL expires.",
    )
    expires_at: datetime | None = Field(
        default=None,
        description="Optional expiration time for the shortened URL.",
    )

    @validator("original_url")
    def validate_original_url(cls, value: HttpUrl) -> HttpUrl:
        if value.scheme not in {"http", "https"}:
            raise ValueError("Only http and https URLs are supported.")

        if len(str(value)) > 2048:
            raise ValueError("URL must be 2048 characters or fewer.")

        return value

    @validator("expiry_days")
    def validate_expiry_days(cls, value: int | None) -> int | None:
        if value is not None and value < 1:
            raise ValueError("expiry_days must be greater than 0.")

        return value

    @validator("expires_at")
    def validate_expires_at(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value

        normalized_value = value
        if normalized_value.tzinfo is None:
            normalized_value = normalized_value.replace(tzinfo=timezone.utc)

        if normalized_value <= datetime.now(timezone.utc):
            raise ValueError("expires_at must be in the future.")

        return value

    @root_validator
    def validate_expiration_inputs(cls, values: dict) -> dict:
        expiry_days = values.get("expiry_days")
        expires_at = values.get("expires_at")
        if expiry_days is not None and expires_at is not None:
            raise ValueError("Provide either expiry_days or expires_at, not both.")

        return values


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    clicks: int
    created_at: datetime | None
    expires_at: datetime | None


class URLStatsResponse(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime | None
    expires_at: datetime | None
