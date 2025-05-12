from abc import abstractmethod
from src.application.data.IUser import IUser
from src.infrastructure.repository.SQL.model.User import User
from typing import List
from uuid import UUID

class UserRepository:
    @abstractmethod
    def createUser(self, data: IUser) -> bool:
        pass

    @abstractmethod
    def checkExistingUserByUsername(self, username) -> bool:
        pass

    @abstractmethod
    def checkExistingUserByEmail(self, email) -> bool:
        pass

    @abstractmethod
    def checkExistingUserByPhone(self, phone) -> bool:
        pass

    @abstractmethod
    def getUserByUsername(self, username) -> User | None:
        pass

    @abstractmethod
    def getUserById(self, id: UUID) -> User | None:
        pass

    @abstractmethod
    def consultarUsuario(self, idUser: str) -> User | bool:
        pass

    @abstractmethod
    def consultarUsuarios(self) -> List[User] | bool:
        pass
