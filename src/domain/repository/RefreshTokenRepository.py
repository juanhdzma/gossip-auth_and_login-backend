from abc import abstractmethod
from src.infrastructure.repository.SQL.model.RefreshToken import RefreshToken
from src.application.data.IRefreshToken import IRefreshToken

class RefreshTokenRepository:
    @abstractmethod
    def createRefreshToken(self, data: IRefreshToken) -> bool:
        pass

    @abstractmethod
    def getRefreshTokenByTokenHash(self, hash: str) -> RefreshToken | bool:
        pass

    @abstractmethod
    def revokeToken(self, hash: str) -> bool:
        pass