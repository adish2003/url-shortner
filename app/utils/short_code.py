import secrets
import string

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import URL

DEFAULT_CODE_LENGTH = 6
CODE_ALPHABET = string.ascii_letters + string.digits


def generate_random_code(length: int = DEFAULT_CODE_LENGTH) -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


def generate_unique_short_code(
    db: Session,
    length: int = DEFAULT_CODE_LENGTH,
    max_attempts: int = 10,
) -> str:
    for _ in range(max_attempts):
        candidate = generate_random_code(length=length)
        existing_url = db.scalar(select(URL).where(URL.short_code == candidate))
        if existing_url is None:
            return candidate

    raise ValueError("Unable to generate a unique short code.")
