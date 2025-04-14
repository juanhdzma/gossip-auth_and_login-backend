from sqlalchemy import Column, String
from src.infrastructure.repository.SQL.model.ModelsCreator import Base
from dataclasses import dataclass


@dataclass
class User(Base):
    __tablename__ = 'user'
    id = Column(String(50), primary_key=True)
    phone = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), unique=False, nullable=False)
    last_name = Column(String(100), unique=False, nullable=False)

    def serialize(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
