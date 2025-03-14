import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.auth.__init__ import sign_in_admin_user
from config.models.base import Base

JELOU_DB_FILE = os.getenv("JELOU_DB_FILE")
engine = create_engine(JELOU_DB_FILE, connect_args={"check_same_thread": False})

# Create a SessionLocal class for DB operations
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = LocalSession()
    try:
        yield db
    finally:
        db.close()
def add_admin_user():
    session = LocalSession()
    user_data = {"email": os.getenv("ADMIN_USER_EMAIL"), "name": os.getenv("ADMIN_USER_NAME"),
                 "password": os.getenv("ADMIN_USER_PASSWORD")}
    sign_in_admin_user(session, user_data)


def init_db():
    #Se crean todas las tablas de laas entidades que hereden de Base(si ya existen no pasa nada)
    Base.metadata.create_all(bind=engine)
    #Se añade a un usuario admin para realizar las peticiones y probar authentication.
    add_admin_user()
