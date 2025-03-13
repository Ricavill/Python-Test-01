from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from config.models.base import Base
from config.error.validation_exception import ValidationException


class User(Base):
    obligatory_fields = ['name', 'email', 'password']
    creation_fields = ['name', 'email', "pass_hash"]
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    pass_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def setattr_from_data(self, data: dict):
        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

    def create(self, user_data: dict):
        if not user_data:
            return None

        required_fields = set(self.creation_fields) - set(user_data.keys())

        if len(required_fields) != 0:
            raise ValidationException(f"Required fields: {required_fields}")
        self.setattr_from_data(user_data)
        return self
