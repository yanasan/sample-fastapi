import datetime
from typing import Optional
from jose import jwt, JWTError
from app.core.config import settings


class AuthUtils:
    @staticmethod
    def create_access_token(sub: str, exp_minutes: int, payload: dict = None) -> str:
        to_encode = {
            "sub": sub,
            "type": "access",
        }
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=exp_minutes)
        to_encode.update({"exp": expire})
        if payload:
            to_encode.update(payload)

        encoded_jwt = AuthUtils._encode_jwt(to_encode)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(sub: str, exp_days: int, payload: dict = None) -> str:
        to_encode = {
            "sub": sub,
            "type": "refresh",
        }
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=exp_days)
        to_encode.update({"exp": expire})
        if payload:
            to_encode.update(payload)

        encoded_jwt = AuthUtils._encode_jwt(to_encode)
        return encoded_jwt

    @staticmethod
    def decode_jwt(token: str) -> dict:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    @staticmethod
    def _encode_jwt(payload: dict) -> str:
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
