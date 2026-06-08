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


@router.post("/validate-otp", response_model=Token)
async def login(
    email: str,
    service: Annotated[UserService, Depends(get_user_service)],
):
    user = await service.create_user(email)
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="Bearer")

