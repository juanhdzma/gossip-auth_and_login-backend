from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.Envs import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


class CloudDatabase:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    def createConnection(self):
        currentSession = sessionmaker(bind=self.engine)
        session = currentSession()
        return session

    def closeConnection(self, session):
        session.close()
