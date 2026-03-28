import os
from dataclasses import dataclass


def _get_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "URL Shortener API")
    VERSION: str = os.getenv("VERSION", "0.1.0")
    DESCRIPTION: str = os.getenv(
        "DESCRIPTION",
        "RESTful API for creating short URLs and handling redirects.",
    )
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    DEBUG: bool = _get_bool(os.getenv("DEBUG"), default=True)
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/url_shortener",
    )
    DATABASE_ECHO: bool = _get_bool(os.getenv("DATABASE_ECHO"), default=False)


settings = Settings()
