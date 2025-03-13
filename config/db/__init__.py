import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.auth.__init import sign_in_admin_user
from config.models.base import Base

JELOU_DB_FILE = os.getenv("JELOU_DB_FILE")
engine = create_engine(JELOU_DB_FILE, connect_args={"check_same_thread": False})

# Create a SessionLocal class for DB operations
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = LocalSession()
    try:
        yield db  # Provide session to request
    finally:
        db.close()  # Ensure session is closed after request
def add_admin_user():
    session = LocalSession()
    user_data = {"email": os.getenv("ADMIN_USER_EMAIL"), "name": os.getenv("ADMIN_USER_NAME"),
                 "password": os.getenv("ADMIN_USER_PASSWORD")}
    sign_in_admin_user(session, user_data)


def init_db():
    Base.metadata.create_all(bind=engine)
    add_admin_user()
