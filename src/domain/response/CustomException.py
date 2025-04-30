from datetime import datetime
from fastapi.encoders import jsonable_encoder
from src.domain.response.StatusCode import StatusCode


class CustomException(Exception):
    def __init__(self, message: str, statusCode: StatusCode):
        self.is_error = True
        self.message = message
        self.status_code = statusCode
        self.timestamp = datetime.now()

    def serialize(self):
        return jsonable_encoder(self)


class BadRequestException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, StatusCode.BAD_REQUEST)


class ConflictException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, StatusCode.CONFLICT)


class InternalServerErrorException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, StatusCode.INTERNAL_SERVER_ERROR)


class NotFoundException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, StatusCode.NOT_FOUND)


class InvalidMethodException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, StatusCode.INVALID_METHOD)


class TeapotException(CustomException):
    def __init__(self, message: str):
        super().__init__(message, StatusCode.TEAPOT)

class Unauthorized(CustomException):
    def __init__(self, message: str):
        super().__init__(message, StatusCode.UNAUTHORIZED)
