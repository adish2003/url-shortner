from typing import Any

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    success: bool = True
    message: str
    data: dict[str, Any] | None = None


class ValidationIssue(BaseModel):
    field: str = Field(..., description="The request field that failed validation.")
    message: str = Field(..., description="The validation error message.")


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list[ValidationIssue] | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
