from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.schemas import URLCreate, URLResponse
from app.services import (
    create_shortened_url,
    get_url_by_short_code,
    increment_click_count,
    is_url_expired,
)

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


@router.get("/{short_code}", tags=["urls"])
def redirect_to_url(short_code: str, db: Session = Depends(get_db)) -> RedirectResponse:
    db_url = get_url_by_short_code(db=db, short_code=short_code)
    if db_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found.",
        )

    if is_url_expired(db_url):
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Short URL has expired.",
        )

    increment_click_count(db=db, db_url=db_url)
    return RedirectResponse(
        url=db_url.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
