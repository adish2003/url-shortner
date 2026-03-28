from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import URL


def create_url(
    db: Session,
    original_url: str,
    short_code: str,
    expires_at: datetime | None = None,
) -> URL:
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


def increment_click_count(db: Session, db_url: URL) -> URL:
    db.execute(
        update(URL)
        .where(URL.id == db_url.id)
        .values(clicks=URL.clicks + 1),
    )
    db.commit()
    db.refresh(db_url)
    return db_url
