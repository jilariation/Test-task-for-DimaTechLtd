import jwt
from datetime import datetime, timedelta, timezone

from app.config import SECRET_JWT_KEY


def create_token(user_id: int, is_admin: bool):
    expiration = datetime.now(timezone.utc) + timedelta(days=1)
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': expiration
    }
    token = jwt.encode(payload, SECRET_JWT_KEY, algorithm='HS256')
    return token


def decode_token(token: str):
    try:
        token = token.split('Bearer ')[1]
        payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
