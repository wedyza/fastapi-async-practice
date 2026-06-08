from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import select, update

from src.app.core.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    UncategorizedException,
)
from src.infrastructure.postgresql.db_engine import async_session_factory
from src.infrastructure.postgresql.models import UsersOrm


@dataclass(slots=True, frozen=True)
class UserRecord:
    id: UUID
    email: str
    is_admin: bool
    otp: Optional[str] = None
    otp_created_at: Optional[datetime] = None


@dataclass(slots=True, frozen=True)
class OtpRecord:
    otp: str
    email: str


class UserRepository:
    async def get_user_by_email(self, email: str) -> UserRecord:
        async with async_session_factory() as session:
            query = (
                select(
                    UsersOrm.id,
                    UsersOrm.email,
                    UsersOrm.is_admin,
                    UsersOrm.otp,
                    UsersOrm.otp_created_at,
                )
                .where(UsersOrm.email == email)
                .limit(1)
            )
            result = await session.execute(query)
            row = result.one_or_none()
            if row is None:
                raise NotFoundException(f"Пользователь с email={email} не найден!")
            id, email, is_admin, otp, otp_created_at = row
            return UserRecord(
                id=id,
                email=email,
                is_admin=is_admin,
                otp=otp,
                otp_created_at=otp_created_at
            )

    async def create_user(self, email: str) -> UserRecord:
        async with async_session_factory() as session:
            user = await self.get_user_by_email(email)
            if user is None:
                created_user = UsersOrm(
                    id=uuid4(),
                    email=email,
                    is_admin=False,
                    otp=None,
                    otp_created_at=None
                )
                session.add(created_user)
                await session.commit()
                return UserRecord(
                    id=created_user.id,
                    email=email,
                    is_admin=created_user.is_admin,
                )
            else:
                raise AlreadyExistsException(f"Пользователь с email={email} уже существует!")

    async def fill_user_otp_data(self, email: str) -> OtpRecord | None:
        generated_otp = "123123"
        async with async_session_factory() as session:
            update_query = (
                update(UsersOrm)
                .where(UsersOrm.email == email)
                .values(
                    otp = generated_otp,
                    otp_created_at=datetime.now(timezone.utc)
                )
                .returning(UsersOrm.id)
            )
            update_result = await session.execute(update_query)
            updated_user_id = update_result.scalar_one_or_none()
            if updated_user_id is None:
                raise UncategorizedException("Что-то пошло не так...")
            await session.commit()
            return OtpRecord(
                otp = generated_otp,
                email = email
            )

    async def clear_user_otp_data(self, email: str) -> None:
        async with async_session_factory() as session:
            update_query = (
                update(UsersOrm)
                .where(UsersOrm.email == email)
                .values(
                    otp = None,
                    otp_created_at=None
                )
                .returning(UsersOrm.id)
            )
            update_result = await session.execute(update_query)
            updated_user_id = update_result.scalar_one_or_none()
            if updated_user_id is None:
                raise UncategorizedException("Что-то пошло не так...")
            await session.commit()
