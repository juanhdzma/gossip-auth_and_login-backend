from fastapi import APIRouter
from src.application.data.IUser import IUser
from src.application.service.UserService import UserService


app_router = APIRouter()
userService = UserService()


@app_router.post("/auth")
def createUser(payload: IUser):
    return userService.createUser(payload)


@app_router.post("/create")
def createUser(payload: IUser):
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
