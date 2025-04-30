from src.application.data.IUser import IUser
from src.application.data.DTOs.CreateUserDto import CreateUserDto
from src.application.service.RefreshTokenService import RefreshTokenService
from src.application.utils.TokenHelper import AccessTokenGoogleHelper, AccessTokenHelper
from src.domain.response.Result import CorrectResult, EntityCreated
from src.domain.response.CustomException import (
    NotFoundException, ConflictException, BadRequestException, Unauthorized
)
from src.domain.response.Response import Response
from src.infrastructure.configuration.DependencyContainer import DependencyContainer
from src.domain.repository.UserRepository import UserRepository
from injector import Injector

class UserService:

    def __init__(self):
        self.injector = Injector([DependencyContainer()])
        self.user_repository = self.injector.get(UserRepository)
        self.refresh_token_service = RefreshTokenService()

    def createUser(self, user: CreateUserDto):
        userToSave=None
        if user.source == "Google":
            result = AccessTokenGoogleHelper.decode_access_token(user.key)
            if result.status_code != 200:
                return Response.failure(Unauthorized(f"Request had invalid authentication credentials: {result.body}"))
            
            userToSave = IUser(
                source=user.source, 
                username=user.username, 
                email=result["email"],
                phone=user.phone,
                full_name= result["name"]
            )
        elif user.source == "Number":
            #Change
            userToSave = IUser(
                source=user.source, 
                username=user.username, 
                email=user.email,
                phone=user.phone,
                full_name= user.full_name
            )
        else: 
            return Response.failure(BadRequestException(f"Source not found"))
        

        existing_user = self.check_existing_user(userToSave) 
        if existing_user!= False: return existing_user 

        createdUser = self.user_repository.createUser(userToSave)

        if createdUser:
            refreshToken=self.refresh_token_service.createRefreshToken(self.user_repository.getUserByUsername(userToSave.username).id)
            if refreshToken == False:
                return Response.failure(ConflictException("it was not possible to generate the refresh token"))
            
            accessToken = AccessTokenHelper.create_access_token(email=userToSave.email, username=userToSave.username)
            return Response.ok(EntityCreated({
                "Refresh_token": refreshToken,
                "Access_token": accessToken
            }))
        return Response.failure(ConflictException("The user already exists"))
    
    def check_existing_user(self, user: IUser) -> Response | bool:
        if self.user_repository.checkExistingUserByUsername(user.username):
            return Response.failure(ConflictException(f"The username already exists: {user.username}"))
        if user.email != None:
            if self.user_repository.checkExistingUserByEmail(user.email):
                return Response.failure(ConflictException(f"The email already exists: {user.email}"))
        if user.phone != None:
            if self.user_repository.checkExistingUserByPhone(user.phone):
                return Response.failure(ConflictException(f"The phone number already exists: {user.phone}"))
        return False
 

# it's no part of this project yet
    def getUser(self, idUser):
        if idUser.isdigit():
            result = self.user_repository.consultarUsuario(idUser)
        else:
            return Response.failure(BadRequestException("Id no valido"))

        if result:
            result = result.serialize()
            return Response.ok(CorrectResult(result))
        return Response.failure(NotFoundException("El usuario no esta en la base de datos"))

    def getAllUsers(self):
        result = self.user_repository.consultarUsuarios()
        if result:
            result = [i.serialize() for i in result]
            return Response.ok(CorrectResult(result))
        return Response.failure(NotFoundException("No hay usuarios en la base de datos"))
