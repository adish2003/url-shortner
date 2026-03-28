from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.schemas import URLCreate, URLResponse
from app.services import create_shortened_url

router = APIRouter()


@router.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs_url": "/docs",
    }


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED, tags=["urls"])
def shorten_url(payload: URLCreate, request: Request, db: Session = Depends(get_db)) -> URLResponse:
    db_url = create_shortened_url(
        db=db,
        original_url=str(payload.original_url),
        expires_at=payload.expires_at,
    )
    short_url = f"{str(request.base_url).rstrip('/')}/{db_url.short_code}"
    return URLResponse(
        id=db_url.id,
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        short_url=short_url,
        clicks=db_url.clicks,
        created_at=db_url.created_at,
        expires_at=db_url.expires_at,
    )
