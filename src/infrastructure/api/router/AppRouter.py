from fastapi import APIRouter
from src.application.data.DTOs.RotateRefreshTokenDto import RotateRefreshTokenDto
from src.application.service.RefreshTokenService import RefreshTokenService
from src.application.data.DTOs.CreateUserDto import CreateUserDto
from src.application.data.IUser import IUser
from src.application.service.UserService import UserService


app_router = APIRouter()
userService = UserService()
refreshTokenService = RefreshTokenService()

@app_router.post("/login")
def createUser(payload: IUser):
    return userService.createUser(payload)

@app_router.post("/create")
def createUser(payload: CreateUserDto):
    return userService.createUser(payload)

@app_router.post("/refresh")
def createUser(payload: RotateRefreshTokenDto):
    return refreshTokenService.rotate_refresh_token(payload.refreshToken)

@app_router.post("/logout")
def createUser(payload: CreateUserDto):
    return userService.createUser(payload)

@app_router.delete("/user")
def createUser(payload: IUser):
    return userService.createUser(payload)


@app_router.patch("/user")
def createUser(payload: IUser):
    return userService.createUser(payload)


@app_router.patch("/keep_login")
def createUser(payload: IUser):
    return userService.createUser(payload)


# @app_router.post("/user")
# def createUser(payload: IUser):
#     return userService.createUser(payload)


# @app_router.get("/user/{idUser}")
# def getUser(idUser):
#     return userService.getUser(idUser)


# @app_router.get("/users")
# def getUsers():
#     return userService.getAllUsers()
