from dataclasses import dataclass
from datetime import datetime,timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, UUID
from src.infrastructure.repository.SQL.model.ModelsCreator import Base

@dataclass
class RefreshToken(Base):
    __tablename__ = "refresh_token"
    token_hash = Column(String, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)

    def serialize(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}