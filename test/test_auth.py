import datetime
import os
from unittest.mock import MagicMock, patch

import bcrypt
import pandas as pd
import pytest
from starlette.testclient import TestClient

from config.auth.__init__ import user_login, sign_in_admin_user, validate_credentials
from config.error import ValidationException
from test import set_secret_key, admin_user, admin_token, user_data,set_db_name
from tweet.tweet_repository import TweetRepository
from user.model import User
from user.user_repository import UserRepository


def test_user_login_success(admin_user, set_secret_key):
    db = MagicMock()
    with (patch("config.auth.__init__.SECRET_KEY", os.getenv("SECRET_KEY")),
          patch.object(UserRepository, "get_by_email", return_value=admin_user) as mock_get_by_email):
        user_data = {"email": "ric@hotmail.com", "password": "ric123"}
        assert user_login(db, user_data) is not None

        mock_get_by_email.assert_called_once_with(db, user_data["email"])


def test_user_login_missing_fields():
    db = MagicMock()
    user_data = {"email": "test@example.com"}  # Missing password
    with pytest.raises(ValidationException, match="Email and password are required."):
        user_login(db, user_data)


def test_sign_in_admin_user_existing_user(admin_user, user_data):
    db = MagicMock()
    with patch.object(UserRepository, "get_by_email", return_value=admin_user) as mock_get_by_email:
        assert sign_in_admin_user(db, user_data) is None  # Admin user already exists
        mock_get_by_email.assert_called_once_with(db, user_data["email"])


def test_sign_in_admin_user_new_user(user_data):
    db = MagicMock()
    user_data = {"name": "ric", "email": "ric@hotmail.com", "password": "ric123"}
    with patch.object(UserRepository, "get_by_email", return_value=User()), patch.object(UserRepository, "get_by_email",
                                                                                         return_value=None):
        user = sign_in_admin_user(db, user_data)
        assert user is not None


def test_validate_credentials_success(admin_user, admin_token, set_secret_key):
    db = MagicMock()
    mock_user = MagicMock()
    t = datetime.datetime(2025, 3, 13, 21, 31, 53, 76473)
    mock_user.pass_hash = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).hex()
    with (patch("utils.jwt_utils.datetime.datetime") as mock_datetime, patch("config.auth.__init__.SECRET_KEY",
                                                                             os.getenv("SECRET_KEY")),
          patch.object(UserRepository, "get_by_email", return_value=admin_user)):
        mock_datetime.now.return_value = t

        assert validate_credentials(db, "ric@hotmail.com", "ric123") == admin_token


def test_validate_credentials_user_not_found():
    db = MagicMock()
    with patch.object(UserRepository, "get_by_email", return_value=None):
        with pytest.raises(ValidationException, match="User with email test@example.com does not exist."):
            validate_credentials(db, "test@example.com", "password123")


def test_validate_credentials_invalid_password(admin_user):
    db = MagicMock()
    with patch.object(UserRepository, "get_by_email", return_value=admin_user):
        assert validate_credentials(db, "test@example.com", "wrong_password") is None

