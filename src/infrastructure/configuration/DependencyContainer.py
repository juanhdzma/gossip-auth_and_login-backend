from injector import inject, Module, singleton
from src.domain.repository.RefreshTokenRepository import RefreshTokenRepository
from src.infrastructure.repository.SQL.dao.RefreshTokenDAO import RefreshTokenDAO
from src.infrastructure.repository.SQL.adapter.SQLiteDatabase import SQLiteDatabase
from src.infrastructure.Envs import ENV
from src.infrastructure.repository.SQL.adapter.CloudDatabase import CloudDatabase
from src.domain.repository.UserRepository import UserRepository
from src.infrastructure.repository.SQL.dao.UserDAO import UserDAO


if ENV == "local":
    database = SQLiteDatabase()
elif ENV == "prod":
    database = CloudDatabase()


class DependencyContainer(Module):
    @singleton
    @inject
    def configure(self, binder):
        binder.bind(UserRepository, to=UserDAO(database))
        binder.bind(RefreshTokenRepository, to=RefreshTokenDAO(database))
