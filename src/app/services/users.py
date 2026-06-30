from datetime import datetime, timedelta, timezone

from src.app.core.exceptions import UncategorizedException, WrongCredentialsException
from src.app.core.redis_settings import enqueue_job  # pyright: ignore[reportUnknownVariableType]
from src.app.repositories.users import UserRepository
from src.app.schemas.users import User


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def register_user(self, email: str) -> User:
        user = await self.create_user(email)
        await self.login_user(user)
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self._repository.get_user_by_email(email)
        return User(
            id=user.id,
            email=user.email,
            is_admin=user.is_admin
        )

    async def create_user(self, email: str) -> User:
        user = await self._repository.create_user(email)
        return User(
            id=user.id,
            email=user.email,
            is_admin=user.is_admin
        )

    async def login_user(self, user: User) -> User:
        # queue = await get_worker_client()
        result = await self._repository.fill_user_otp_data(user.email)
        if result is None:
            raise UncategorizedException('Возникла проблема во время отправки сообщения')
        await enqueue_job('send_email_with_otp', to_email=result.email, otp=result.otp)
        return user

    async def validate_user_otp(self, email: str, otp: str) -> bool:
        user = await self._repository.get_user_by_email(email)
        valid_time = datetime.now(timezone.utc) - timedelta(minutes=15)
        if user.otp == otp and user.otp_created_at > valid_time:  # pyright: ignore[reportOptionalMemberAccess, reportOptionalOperand]
            await self._repository.clear_user_otp_data(email)
            return True
        wrong_pass = user.otp != otp
        error_message = "Неправильный пароль" if wrong_pass else "Время действия пароля вышло"
        raise WrongCredentialsException(error_message)
