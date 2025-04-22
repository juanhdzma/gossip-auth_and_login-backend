from datetime import datetime
from pydantic import BaseModel

class IRefreshToken(BaseModel):
    token_hash: str
    user_name: str
    expires_at: datetime