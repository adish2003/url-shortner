from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.crud import create_url as create_url_record
from app.crud import get_url_by_short_code as get_url_by_short_code_record
from app.crud import increment_click_count as increment_click_count_record
from app.models import URL
from app.utils import generate_unique_short_code


def create_shortened_url(
    db: Session,
    original_url: str,
    expiry_days: int | None = None,
    expires_at: datetime | None = None,
) -> URL:
    short_code = generate_unique_short_code(db)
    return create_url_record(
        db=db,
        original_url=original_url,
        short_code=short_code,
        expires_at=resolve_expiration(expiry_days=expiry_days, expires_at=expires_at),
    )


def get_url_by_short_code(db: Session, short_code: str) -> URL | None:
    return get_url_by_short_code_record(db=db, short_code=short_code)


def is_url_expired(db_url: URL) -> bool:
    if db_url.expires_at is None:
        return False

    if db_url.expires_at.tzinfo is None:
        return db_url.expires_at <= datetime.utcnow()

    return db_url.expires_at <= datetime.now(timezone.utc)


def resolve_expiration(
    expiry_days: int | None = None,
    expires_at: datetime | None = None,
) -> datetime | None:
    if expires_at is not None:
        return expires_at

    if expiry_days is None:
        return None

    return datetime.now(timezone.utc) + timedelta(days=expiry_days)


def increment_click_count(db: Session, db_url: URL) -> URL:
    return increment_click_count_record(db=db, db_url=db_url)
