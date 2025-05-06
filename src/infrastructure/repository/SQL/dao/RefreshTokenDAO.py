from sqlalchemy import and_
from src.application.data.IRefreshToken import IRefreshToken
from src.infrastructure.repository.SQL.model.RefreshToken import RefreshToken
from src.domain.repository.RefreshTokenRepository import RefreshTokenRepository

class RefreshTokenDAO(RefreshTokenRepository):
    def __init__(self, database):
        self.database = database
        
    def createRefreshToken(self, IRefreshToken : IRefreshToken) -> bool:
        try:
            session = self.database.createConnection()
            newRefreshToken = RefreshToken(**IRefreshToken.model_dump())
            session.add(newRefreshToken)
            session.commit()
            return True
        except BaseException as e:
            print(e)
            raise Exception(f"A error happend in create refresh token"); 
        finally:
            self.database.closeConnection(session)

    def getRefreshTokenByTokenHash(self, hash: str) -> RefreshToken | bool:
        try:
            session = self.database.createConnection()
            refreshToken = session.query(RefreshToken).filter(RefreshToken.token_hash == hash).first()
            if refreshToken != None:
                return refreshToken
            return False
        except BaseException as e:
            raise Exception(f"A error happend getting the refresh token"); 
        finally:
            self.database.closeConnection(session)

    def revokeToken(self, hash: str) -> bool:
        try:
            session = self.database.createConnection()
            refreshToken = session.query(RefreshToken).filter(and_(RefreshToken.token_hash == hash, RefreshToken.revoked==False)).first()
            if refreshToken == None:
                return False
            refreshToken.revoked = True
            session.commit()
            return True
        except BaseException as e:
            raise Exception(f"A error happend revoking refresh token Changes"); 
        finally:
            self.database.closeConnection(session)
    