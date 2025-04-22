from datetime import datetime,timedelta, timezone
import hashlib
import uuid
from injector import Injector
from src.domain.response.Result import EntityCreated
from src.domain.repository.UserRepository import UserRepository
from src.domain.response.Response import Response
from src.application.data.IRefreshToken import IRefreshToken
from src.domain.repository.RefreshTokenRepository import RefreshTokenRepository
from src.infrastructure.configuration.DependencyContainer import DependencyContainer
from src.infrastructure.Envs import REFRESH_TOKEN_EXPIRE_MINUTES
from src.domain.response.CustomException import (
    Unauthorized, ConflictException, NotFoundException
)
from src.application.utils.TokenHelper import AccessTokenHelper


class RefreshTokenService:

    def __init__(self):
        self.injector = Injector([DependencyContainer()])
        self.refresh_token_repository = self.injector.get(RefreshTokenRepository)
        self.user_repository = self.injector.get(UserRepository)


    def hash_token(self, token: str) -> str | bool :
        return hashlib.sha256(token.encode()).hexdigest()

    def createRefreshToken(self, user_name: str):
        raw_token = str(uuid.uuid4())
        token_hash = self.hash_token(raw_token)
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        new_refresh_token = IRefreshToken(token_hash = token_hash, user_name=user_name, expires_at = expire)

        result = self.refresh_token_repository.createRefreshToken(new_refresh_token)
        if result:
            return raw_token
        return False
    
    def rotate_refresh_token(self, raw_token: str):
        tokenHash = self.hash_token(raw_token)
        tokenDb = self.refresh_token_repository.getRefreshTokenByTokenHash(tokenHash)

        if not tokenDb or tokenDb.revoked:
            return Response.failure(Unauthorized("Invalid refresh token"))
        if tokenDb.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return Response.failure(Unauthorized("Expired refresh token"))

        currentUser =self.user_repository.getUserByUsername(tokenDb.user_name)
        if currentUser == None:
            return Response.failure(NotFoundException("user not found"))

        revokeToken=self.refresh_token_repository.revokeToken(tokenHash)
        if revokeToken == False:
            return Response.failure(NotFoundException("it was not possible to revoke the token"))

        newRefreshToken = self.createRefreshToken(currentUser.username)
        if newRefreshToken == False:
            return Response.failure(ConflictException("it was not possible to generate the refresh token"))
        
        currentUser =self.user_repository.getUserByUsername(tokenDb.user_name)
        newAccessToken =  AccessTokenHelper.create_access_token(email=currentUser.email, username=currentUser.username)
        
        return Response.ok(EntityCreated({
                "Refresh_token": newRefreshToken,
                "Access_token": newAccessToken
        }))








