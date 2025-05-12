from pydantic import BaseModel

class CreateUserDto(BaseModel):
    username: str
    email: str
    password: str
    phone: str
    full_name: str
    source: str
    key: str