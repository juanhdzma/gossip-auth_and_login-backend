from pydantic import BaseModel

class RotateRefreshTokenDto(BaseModel):
    refreshToken: str