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
        self.refreshTokenRepository = self.injector.get(RefreshTokenRepository)
        self.userRepository = self.injector.get(UserRepository)


    def hashToken(self, token: str) -> str | bool :
        return hashlib.sha256(token.encode()).hexdigest()

    def createRefreshToken(self, userId: UUID):
        rawToken = str(uuid.uuid4())
        tokenHash = self.hashToken(rawToken)
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        newRefreshToken = IRefreshToken(token_hash = tokenHash, user_id=userId, expires_at = expire)

        result = self.refreshTokenRepository.createRefreshToken(newRefreshToken)
        if result:
            return rawToken
        return False
    
    def rotateRefreshToken(self, rawToken: str):
        tokenHash = self.hashToken(rawToken)
        tokenDb = self.refreshTokenRepository.getRefreshTokenByTokenHash(tokenHash)

        if not tokenDb or tokenDb.revoked:
            return Response.failure(Unauthorized("Invalid refresh token"))
        if tokenDb.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return Response.failure(Unauthorized("Expired refresh token"))

        currentUser =self.userRepository.getUserById(tokenDb.user_id)
        if currentUser == None:
            return Response.failure(NotFoundException("user not found with refresh token"))

        revokeToken=self.refreshTokenRepository.revokeToken(tokenHash)
        if revokeToken == False:
            return Response.failure(NotFoundException("it was not possible to revoke the token"))

        newRefreshToken = self.createRefreshToken(currentUser.id)
        if newRefreshToken == False:
            return Response.failure(ConflictException("it was not possible to generate the refresh token"))
        
        newAccessToken =  AccessTokenHelper.createAccessToken(email=currentUser.email, username=currentUser.username)
        
        return Response.ok(EntityCreated({
                "RefreshToken": newRefreshToken,
                "AccessToken": newAccessToken
        }))
    
    def logout(self, refreshToken: str, user: dict):
        tokenHash = self.hashToken(refreshToken)
        tokenDb = self.refreshTokenRepository.getRefreshTokenByTokenHash(tokenHash)
        if not tokenDb or tokenDb.revoked:
            return Response.failure(Unauthorized("Invalid refresh token"))
        if tokenDb.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return Response.failure(Unauthorized("Expired refresh token"))
        
        refreshTokenUser =self.userRepository.getUserById(tokenDb.user_id)
        if refreshTokenUser == None:
            return Response.failure(NotFoundException("user not found with refresh token"))
        
        if refreshTokenUser.username != user["username"]:
            return Response.failure(Unauthorized("The access token and refresh token do not match"))
        
        revokeToken=self.refreshTokenRepository.revokeToken(tokenHash)
        if revokeToken == False:
            return Response.failure(NotFoundException("it was not possible to revoke the token"))

        return Response.ok(CorrectResult({"message": "Logout successful"}))
    





