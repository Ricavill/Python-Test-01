from sqlalchemy.orm import Session

from models.entity_repository import EntityRepository
from user.model import User


class UserRepository(EntityRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db_session: Session, email: str) -> User:
        query = db_session.query(User).filter_by(email=email)
        return self.first(query)
