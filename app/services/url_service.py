from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import URL
from app.utils import generate_unique_short_code


def create_shortened_url(
    db: Session,
    original_url: str,
    expires_at: datetime | None = None,
) -> URL:
    short_code = generate_unique_short_code(db)
    db_url = URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_short_code(db: Session, short_code: str) -> URL | None:
    return db.scalar(select(URL).where(URL.short_code == short_code))


def is_url_expired(db_url: URL) -> bool:
    if db_url.expires_at is None:
        return False

    if db_url.expires_at.tzinfo is None:
        return db_url.expires_at <= datetime.utcnow()

    return db_url.expires_at <= datetime.now(timezone.utc)


def increment_click_count(db: Session, db_url: URL) -> URL:
    db.execute(
        update(URL)
        .where(URL.id == db_url.id)
        .values(clicks=URL.clicks + 1),
    )
    db.commit()
    db.refresh(db_url)
    return db_url
