import http


class RuntimeException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class ModelSetupException(RuntimeException):
    """Exception for failure while loading a model"""


class HttpError(RuntimeException):
    def __init__(self, status_code: http.HTTPStatus, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class BadRequest(HttpError):
    def __init__(self, message):
        super().__init__(http.HTTPStatus.BAD_REQUEST, message)


class InternalServerError(HttpError):
    def __init__(self, message):
        super().__init__(http.HTTPStatus.INTERNAL_SERVER_ERROR, message)
