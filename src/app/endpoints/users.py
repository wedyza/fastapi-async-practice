from fastapi import APIRouter, Depends

from src.app.core.dependencies import get_current_user
from src.app.schemas import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get(path="/me", response_model=User)
async def get_active_user(current_user: User = Depends(get_current_user)):
    return current_user
