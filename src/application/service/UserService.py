from src.application.utils.PasswordHelper import PasswordHelper
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
        self.userRepository = self.injector.get(UserRepository)
        self.refreshTokenService = RefreshTokenService()

    def createUser(self, user: CreateUserDto):
        userToSave=None
        if user.source == "Google":
            result = AccessTokenGoogleHelper.decodeAccessToken(user.key)
            if result.status_code != 200:
                return Response.failure(Unauthorized(f"Request had invalid authentication credentials: {result.body}"))
            
            try:
                userToSave = IUser(
                    source=user.source, 
                    username=user.username,
                    password= PasswordHelper.hashPassword(user.password),
                    email=result["email"],
                    phone=user.phone,
                    full_name= result["name"]
                )
            except BadRequestException as e:
                return Response.failure(e)
             
        elif user.source == "Number":
            #Change
            try:
                userToSave = IUser(
                    source=user.source, 
                    username=user.username, 
                    email=user.email,
                    password= PasswordHelper.hashPassword(user.password),
                    phone=user.phone,
                    full_name= user.full_name
                )
            except BadRequestException as e:
                return Response.failure(e)
        else: 
            return Response.failure(BadRequestException(f"Source not found"))
        

        existingUser = self.checkExistingUser(userToSave) 
        if existingUser!= False: return existingUser 

        createdUser = self.userRepository.createUser(userToSave)

        if createdUser:
            refreshToken=self.refreshTokenService.createRefreshToken(self.userRepository.getUserByUsername(userToSave.username).id)
            if refreshToken == False:
                return Response.failure(ConflictException("it was not possible to generate the refresh token"))
            
            accessToken = AccessTokenHelper.createAccessToken(email=userToSave.email, username=userToSave.username)
            return Response.ok(EntityCreated({
                "RefreshToken": refreshToken,
                "AccessToken": accessToken
            }))
        return Response.failure(ConflictException("The user already exists"))
    
    def checkExistingUser(self, user: IUser) -> Response | bool:
        if self.userRepository.checkExistingUserByUsername(user.username):
            return Response.failure(ConflictException(f"The username already exists: {user.username}"))
        if user.email != None:
            if self.userRepository.checkExistingUserByEmail(user.email):
                return Response.failure(ConflictException(f"The email already exists: {user.email}"))
        if user.phone != None:
            if self.userRepository.checkExistingUserByPhone(user.phone):
                return Response.failure(ConflictException(f"The phone number already exists: {user.phone}"))
        return False
 

# it's no part of this project yet
    def getUser(self, idUser):
        if idUser.isdigit():
            result = self.userRepository.consultarUsuario(idUser)
        else:
            return Response.failure(BadRequestException("Id no valido"))

        if result:
            result = result.serialize()
            return Response.ok(CorrectResult(result))
        return Response.failure(NotFoundException("El usuario no esta en la base de datos"))

    def getAllUsers(self):
        result = self.userRepository.consultarUsuarios()
        if result:
            result = [i.serialize() for i in result]
            return Response.ok(CorrectResult(result))
        return Response.failure(NotFoundException("No hay usuarios en la base de datos"))
