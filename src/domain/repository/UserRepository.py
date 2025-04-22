from abc import abstractmethod
from src.application.data.IUser import IUser
from src.infrastructure.repository.SQL.model.User import User
from typing import List


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

    def getUserByUsername(self, username) -> User | None:
        pass

    @abstractmethod
    def consultarUsuario(self, idUser: str) -> User | bool:
        pass

    @abstractmethod
    def consultarUsuarios(self) -> List[User] | bool:
        pass
