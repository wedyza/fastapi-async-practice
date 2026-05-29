from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

def get_password_hash(password: str) -> str:
    """Хэширование пароля"""
    return pwd_context.hash(password)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:  # pyright: ignore[reportExplicitAny]
    """Создание access токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict[str, Any]) -> str:  # pyright: ignore[reportExplicitAny]
    """Создание refresh токена"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict[str, Any] | None:  # pyright: ignore[reportExplicitAny]
    """Декодирование токена"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
