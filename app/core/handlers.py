from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError
from app.schemas import ErrorDetail, ErrorResponse, ValidationIssue


def _error_response(status_code: int, code: str, message: str, details: list[ValidationIssue] | None = None) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorDetail(code=code, message=message, details=details),
    )
    return JSONResponse(status_code=status_code, content=payload.dict())


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return _error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
    )


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    return _error_response(
        status_code=exc.status_code,
        code="http_error",
        message=message,
    )


async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    issues = [
        ValidationIssue(
            field=".".join(str(part) for part in error["loc"] if part != "body"),
            message=error["msg"],
        )
        for error in exc.errors()
    ]
    return _error_response(
        status_code=422,
        code="validation_error",
        message="Invalid request payload.",
        details=issues,
    )


async def unexpected_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return _error_response(
        status_code=500,
        code="internal_server_error",
        message="An unexpected error occurred.",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
