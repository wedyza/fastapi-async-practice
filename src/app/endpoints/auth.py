from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.core.dependencies import get_user_service
from src.app.core.security import create_access_token
from src.app.schemas import Token, UserCreate
from src.app.services import UserService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(path="/register", response_model=UserCreate)
async def register(email: str, service: Annotated[UserService, Depends(get_user_service)]):
    user = await service.register_user(email)
    return UserCreate(
        email=user.email,
        success=True
    )


@router.post(path="/login", response_model=UserCreate)
async def login(email: str, service: Annotated[UserService, Depends(get_user_service)]):
    user = await service.get_user_by_email(email)
    await service.login_user(user)
    return UserCreate(
        email=user.email,
        success=True
    )


@router.post("/validate-otp", response_model=Token)
async def validate_otp(
    email: str,
    otp: str,
    service: Annotated[UserService, Depends(get_user_service)],
):
    result = await service.validate_user_otp(email, otp)
    if result:
        access_token = create_access_token(data={"sub": email})
        return Token(access_token=access_token, token_type="Bearer")
