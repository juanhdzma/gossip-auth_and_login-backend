from src.infrastructure.repository.SQL.model.User import User
from src.domain.repository.UserRepository import UserRepository


class UserDAO(UserRepository):
    def __init__(self, database):
        self.database = database

    def crearUsuario(self, IUser):
        try:
            session = self.database.createConnection()
            new_user = User(**IUser)
            session.add(new_user)
            session.commit()
            return True
        except BaseException:
            return False
        finally:
            self.database.closeConnection(session)

    def consultarUsuario(self, idUser):
        try:
            session = self.database.createConnection()
            user = session.query(User).filter_by(id=idUser).first()
            return user
        except BaseException:
            return False
        finally:
            self.database.closeConnection(session)

    def consultarUsuarios(self):
        try:
            session = self.database.createConnection()
            users = session.query(User).all()
            return users
        except BaseException as error:
            print(error)
            return False
        finally:
            self.database.closeConnection(session)
