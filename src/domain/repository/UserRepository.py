from abc import abstractmethod
from src.application.data.IUser import IUser
from src.infrastructure.repository.SQL.model.User import User
from typing import List


class UserRepository:
    @abstractmethod
    def crearUsuario(self, data: IUser) -> bool:
        pass

    @abstractmethod
    def consultarUsuario(self, idUser: str) -> User | bool:
        pass

    @abstractmethod
    def consultarUsuarios(self) -> List[User] | bool:
        pass
