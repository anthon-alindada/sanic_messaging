# -*- coding: utf-8
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from datetime import datetime, timedelta
from . import app


def encode_jwt(payload):
    """
    Encode jwt
    """
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256').decode("utf-8")

    return token


def decode_jwt(token):
    """
    Decode jwt
    """
    try:
        payload = jwt.decode(
            token, app.config.get('SECRET_KEY'), algorithm=['HS256'])
    except DecodeError:
        return {}
    except ExpiredSignatureError:
        return {}

    return payload


def generate_auth_jwt(user_id, email):
    """
    Generate auth user jwt
    """
    payload = {
        'type': 'authentication',
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }

    token = encode_jwt(payload)

    return token
