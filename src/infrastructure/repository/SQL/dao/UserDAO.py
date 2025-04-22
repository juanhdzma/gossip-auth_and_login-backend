from src.application.data.IUser import IUser
from src.infrastructure.repository.SQL.model.User import User
from src.domain.repository.UserRepository import UserRepository
from uuid import UUID

class UserDAO(UserRepository):
    def __init__(self, database):
        self.database = database

    def createUser(self, user: IUser):
        try:
            session = self.database.createConnection()
            new_user = User(**user.model_dump())
            session.add(new_user)
            session.commit()
            return True
        except BaseException as e:
            print(e)
            return False
        finally:
            self.database.closeConnection(session)

    def checkExistingUserByUsername(self, username):
        try:
            session = self.database.createConnection()
            user = session.query(User).filter(User.username == username).first()
            if user != None:
                return True
            return False
        except BaseException as e:
            print("error: ", e)
            raise Exception(f"A error happend in checkExistingUserByUsername"); 
        finally:
            self.database.closeConnection(session)

    def checkExistingUserByEmail(self, email):
        try:
            session = self.database.createConnection()
            user = session.query(User).filter(User.email == email).first()
            if user != None:
                return True
            return False
        except BaseException as e:
            raise Exception(f"A error happend in checkExistingUserByEmail"); 
        finally:
            self.database.closeConnection(session)

    def checkExistingUserByPhone(self, phone):
        try:
            session = self.database.createConnection()
            user = session.query(User).filter(User.phone == phone).first()
            if user != None:
                return True
            return False
        except BaseException as e:
            raise Exception(f"A error happend in checkExistingUserByPhone"); 
        finally:
            self.database.closeConnection(session)

    def getUserByUsername(self, username) -> User | None:
        try:
            session = self.database.createConnection()
            user = session.query(User).filter(User.username == username).first()
            return user
        except BaseException:
            raise Exception(f"A error happend in getUserByUsername"); 
        finally:
            self.database.closeConnection(session)

    def getUserById(self, id: UUID) -> User | None:
        try:
            session = self.database.createConnection()
            user = session.query(User).filter(User.id == id).first()
            return user
        except BaseException:
            raise Exception(f"A error happend in getUserById"); 
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


    
