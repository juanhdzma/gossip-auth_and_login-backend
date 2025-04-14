from fastapi.responses import JSONResponse
from typing import TypeVar
from src.domain.response.CustomException import CustomException

T = TypeVar('T')


class Response:
    @staticmethod
    def ok(data: T) -> JSONResponse:
        return JSONResponse(content=data.serialize(), status_code=data.status_code.value)

    @staticmethod
    def failure(exception: CustomException) -> JSONResponse:
        return JSONResponse(content=exception.serialize(), status_code=exception.status_code.value)
