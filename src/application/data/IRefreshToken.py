from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class IRefreshToken(BaseModel):
    token_hash: str
    user_id: UUID
    expires_at: datetime