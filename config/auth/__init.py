import os

import bcrypt
from sqlalchemy.orm import Session

from config.error.validation_exception import ValidationException
from user.model import User
from user.schema import UserSchema
from user.user_repository import UserRepository
from utils.jwt_utils import get_token_from_data

SECRET_KEY = os.getenv('JWT_SECRET_KEY')


# Asi sea que no tengamos pantalla de login, con esta función podre conseguir el token de usuario
def user_login(db: Session, user_data: dict):
    password = user_data.get('password')
    email = user_data.get('email')
    if not email or not password:
        raise ValidationException('Email and password are required.')
    return validate_credentials(db, email, password)


def sign_in_admin_user(db: Session, user_data: dict):
    password = user_data.get('password')
    required_fields = set(User.obligatory_fields) - set(user_data.keys())
    if len(required_fields) != 0:
        raise ValidationException(f"Required fields missing: {required_fields}")
    user_repository = UserRepository()
    admin_user = user_repository.get_by_email(db, user_data.get("email"))
    if admin_user:
        return None
    pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).hex()
    user_data['pass_hash'] = pass_hash
    user = User().create(user_data)
    user_repository.save(db, user)


def validate_credentials(db: Session, email: str, password: str):
    user = UserRepository().get_by_email(db, email)
    if not user:
        raise ValidationException(f'User with email {email} does not exist.')
    hashed_password = user.pass_hash
    hashed_password = bytes.fromhex(hashed_password)
    if bcrypt.checkpw(password.encode(), hashed_password):
        authenticated_user = UserSchema().dump(user)
        return get_token_from_data(authenticated_user, SECRET_KEY)
    else:
        return None
