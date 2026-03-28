class AppError(Exception):
    status_code = 400
    code = "app_error"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ResourceNotFoundError(AppError):
    status_code = 404
    code = "not_found"


class ResourceExpiredError(AppError):
    status_code = 410
    code = "expired"
