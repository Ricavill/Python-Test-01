import datetime

import jwt
import pytest
from jwt import InvalidTokenError

from config.error import UnauthorizedException
from utils.jwt_utils import get_token_from_data, decode_token


def test_get_token_from_data():
    secret_key = "test_secret"
    data = {"user_id": 123}
    token = get_token_from_data(data, secret_key)
    assert token is not None
    assert isinstance(token, str)


def test_get_token_from_data_with_empty_data():
    secret_key = "test_secret"
    data = {}
    token = get_token_from_data(data, secret_key)
    assert token is None


def test_decode_token():
    secret_key = "test_secret"
    data = {"user_id": 123}
    token = get_token_from_data(data, secret_key)
    decoded_data = decode_token(token, secret_key)
    assert decoded_data is not None
    assert "user_id" in decoded_data
    assert decoded_data["user_id"] == 123


def test_decode_token_with_invalid_token():
    secret_key = "test_secret"
    invalid_token = "invalid.token.string"
    with pytest.raises(UnauthorizedException, match="Invalid token"):
        decode_token(invalid_token, secret_key)


def test_decode_token_with_expired_token():
    secret_key = "test_secret"
    data = {"user_id": 123, "exp": datetime.datetime.now() - datetime.timedelta(seconds=1)}
    expired_token = jwt.encode(data, secret_key, algorithm='HS256')
    with pytest.raises(UnauthorizedException, match="Token has expired"):
        decode_token(expired_token, secret_key)
