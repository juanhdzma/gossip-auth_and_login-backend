from dotenv import load_dotenv
import os

os.environ.clear()
load_dotenv(".env")
ENV = os.getenv("ENV")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
REFRESH_TOKEN_EXPIRE_MINUTES=float(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_EXPIRE_MINUTES=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM=os.getenv("ALGORITHM")
SECRET_KEY=os.getenv("SECRET_KEY")

print("ENV RUNNING:", ENV)
