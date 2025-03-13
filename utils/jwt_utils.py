import datetime

import jwt

from config.error import UnauthorizedException


def get_token_from_data(data: dict, secret_key: str):
    if not data or type(data) is not dict:
        return None
    try:
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=300000)
        data['exp'] = expiration_time
        encoded = jwt.encode(data, secret_key, algorithm='HS256')
        return encoded
    except Exception as e:
        return None


def decode_token(token, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")
