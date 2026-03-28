from fastapi import APIRouter

from app.core.config import settings

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

