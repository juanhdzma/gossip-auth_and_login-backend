from passlib.context import CryptContext
import bcrypt
bcrypt.__about__ = bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHelper:
    @staticmethod
    def hashPassword(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
        return pwd_context.verify(plainPassword, hashedPassword)