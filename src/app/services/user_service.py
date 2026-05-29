from src.app.repositories.users import UserRepository
from src.app.schemas.users import User


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self._repository.get_user_by_email(email)
        return User(
            id=user.id,
            email=user.email,
            is_admin=user.is_admin
        ) if user else None

    async def get_or_create_user_by_email(self, email: str) -> User:
        user = await self._repository.get_or_create_user_by_email(email)
        return User(
            id=user.id,
            email=user.email,
            is_admin=user.is_admin
        )
