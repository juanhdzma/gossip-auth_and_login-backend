from pydantic import BaseModel, field_validator


class IUser(BaseModel):
    username: str
    email: str
    phone: str
    full_name: str
    source: str
    active: bool = True
    keep_login: bool = True

    @field_validator("phone")
    def validatePhone(cls, value):
        if value.isdigit() and len(value) == 10:
            return value
        raise ValueError("Phone number is not valid")

    @field_validator("full_name")
    def validateName(cls, value):
        parts = value.split()
        for part in parts:
            if not part.isalpha():
                raise ValueError("The full name is not valid")
        return value
