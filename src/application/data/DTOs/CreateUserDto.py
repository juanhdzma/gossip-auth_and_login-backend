from pydantic import BaseModel

class CreateUserDto(BaseModel):
    username: str
    email: str
    phone: str
    full_name: str
    source: str
    key: str