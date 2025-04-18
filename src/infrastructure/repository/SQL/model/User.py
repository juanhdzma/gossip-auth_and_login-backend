from sqlalchemy import Column, String
from src.infrastructure.repository.SQL.model.ModelsCreator import Base
from dataclasses import dataclass


@dataclass
class User(Base):
    __tablename__ = "user"
    username = Column(String(60), primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    full_name = Column(String(100), unique=False, nullable=False)
    source = Column(String(100), unique=False, nullable=False)
    active = Column(String(100), unique=False, nullable=False)
    keep_login = Column(String(100), unique=False, nullable=False)

    def serialize(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
