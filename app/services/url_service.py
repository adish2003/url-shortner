from datetime import datetime

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
