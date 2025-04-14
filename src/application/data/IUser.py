from pydantic import BaseModel, field_validator


class IUser(BaseModel):
    id: str
    phone: str
    name: str
    last_name: str

    @field_validator("id")
    def validateId(cls, value):
        if value.isdigit():
            return value
        raise ValueError("La cedula no es valida")

    @field_validator("phone")
    def validatePhone(cls, value):
        if value.isdigit() and len(value) == 10:
            return value
        raise ValueError("El telefono no es valido")

    @field_validator("name", "last_name")
    def validateName(cls, value):
        parts = value.split()
        for part in parts:
            if not part.isalpha():
                raise ValueError("El nombre o apellido no son validos")
        return value
