from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.app.core.exceptions import NotFoundException
from src.app.core.security import decode_token
from src.app.repositories import UserRepository
from src.app.schemas.users import User
from src.app.services import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_user_repostory() -> AsyncIterator[UserRepository]:
    yield UserRepository()

async def get_user_service(repository: Annotated[UserRepository, Depends(get_user_repostory)]):
    yield UserService(repository=repository)


async def auth_user(
    service: Annotated[UserService, Depends(get_user_service)],
    token: str = Depends(oauth2_scheme)
    ) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")  # pyright: ignore[reportAssignmentType]
    if email is None:  # pyright: ignore[reportUnnecessaryComparison]
        raise credentials_exception
    try:
        user = await service.get_user_by_email(email)
    except NotFoundException as err:
        raise credentials_exception from err

    return user
