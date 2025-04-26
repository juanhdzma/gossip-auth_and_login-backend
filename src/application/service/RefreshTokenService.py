from datetime import datetime,timedelta, timezone
import hashlib
import uuid
from uuid import UUID
from injector import Injector
from src.domain.response.Result import CorrectResult, EntityCreated
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

    def createRefreshToken(self, user_id: UUID):
        raw_token = str(uuid.uuid4())
        token_hash = self.hash_token(raw_token)
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        new_refresh_token = IRefreshToken(token_hash = token_hash, user_id=user_id, expires_at = expire)

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

        currentUser =self.user_repository.getUserById(tokenDb.user_id)
        if currentUser == None:
            return Response.failure(NotFoundException("user not found with refresh token"))

        revokeToken=self.refresh_token_repository.revokeToken(tokenHash)
        if revokeToken == False:
            return Response.failure(NotFoundException("it was not possible to revoke the token"))

        newRefreshToken = self.createRefreshToken(currentUser.id)
        if newRefreshToken == False:
            return Response.failure(ConflictException("it was not possible to generate the refresh token"))
        
        newAccessToken =  AccessTokenHelper.create_access_token(email=currentUser.email, username=currentUser.username)
        
        return Response.ok(EntityCreated({
                "Refresh_token": newRefreshToken,
                "Access_token": newAccessToken
        }))
    
    def logout(self, refresh_token: str, user: dict):
        tokenHash = self.hash_token(refresh_token)
        tokenDb = self.refresh_token_repository.getRefreshTokenByTokenHash(tokenHash)
        if not tokenDb or tokenDb.revoked:
            return Response.failure(Unauthorized("Invalid refresh token"))
        if tokenDb.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return Response.failure(Unauthorized("Expired refresh token"))
        
        refreshTokenUser =self.user_repository.getUserById(tokenDb.user_id)
        if refreshTokenUser == None:
            return Response.failure(NotFoundException("user not found with refresh token"))
        
        if refreshTokenUser.username != user["username"]:
            return Response.failure(Unauthorized("The access token and refresh token do not match"))
        
        revokeToken=self.refresh_token_repository.revokeToken(tokenHash)
        if revokeToken == False:
            return Response.failure(NotFoundException("it was not possible to revoke the token"))

        return Response.ok(CorrectResult({"message": "Logout successful"}))
    





