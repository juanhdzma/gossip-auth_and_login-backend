from pydantic import BaseModel, field_validator
from src.domain.response.CustomException import BadRequestException

class IUser(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    full_name: str
    source: str
    active: bool = True
    keep_login: bool = True

    @field_validator("phone")
    def validatePhone(cls, value):
        if value.isdigit() and len(value) == 10:
            return value
        raise BadRequestException(f"The phone number is not valid")

    @field_validator("full_name")
    def validateName(cls, value):
        parts = value.split()
        for part in parts:
            if not part.isalpha():
                raise BadRequestException("The full name is not valid")
        return value
