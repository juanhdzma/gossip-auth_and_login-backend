from typing import TypeVar
from datetime import datetime
from src.domain.response.StatusCode import StatusCode
from fastapi.encoders import jsonable_encoder

T = TypeVar('T')


class Result:
    def __init__(self, data: T, statusCode: StatusCode):
        self.isError = False
        self.data = data
        self.statusCode = statusCode
        self.timestamp = datetime.now()

    def serialize(self):
        return jsonable_encoder(self)


class CorrectResult(Result):
    def __init__(self, data: T):
        super().__init__(data, StatusCode.OK)


class EntityCreated(Result):
    def __init__(self, data: T):
        super().__init__(data, StatusCode.CREATED)
