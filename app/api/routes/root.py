from fastapi import APIRouter

from app.core.config import settings
from app.schemas import MessageResponse

router = APIRouter()


@router.get("/", response_model=MessageResponse, tags=["root"])
def read_root() -> MessageResponse:
    return MessageResponse(
        message=f"Welcome to {settings.PROJECT_NAME}",
        data={"docs_url": "/docs"},
    )


@router.get("/health", response_model=MessageResponse, tags=["health"])
def health_check() -> MessageResponse:
    return MessageResponse(
        message="Service is healthy.",
        data={"status": "ok"},
    )
