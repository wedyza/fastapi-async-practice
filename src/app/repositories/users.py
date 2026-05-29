from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy import select

from src.infrastructure.postgresql.db_engine import async_session_factory
from src.infrastructure.postgresql.models import UsersOrm


@dataclass(slots=True, frozen=True)
class UserRecord:
    id: UUID
    email: str
    is_admin: bool


class UserRepository:
    async def get_user_by_email(self, email: str) -> UserRecord | None:
        async with async_session_factory() as session:
            query = select(UsersOrm.id, UsersOrm.email, UsersOrm.is_admin).where(UsersOrm.email == email).limit(1)
            result = await session.execute(query)
            row = result.one_or_none()
            if row is None:
                return None
            id, email, is_admin = row
            return UserRecord(
                id=id,
                email=email,
                is_admin=is_admin
            )

    async def get_or_create_user_by_email(self, email: str) -> UserRecord:
        async with async_session_factory() as session:
            user = await self.get_user_by_email(email)
            if user is None:
                created_user = UsersOrm(
                    id=uuid4(),
                    email=email,
                    is_admin=False
                )
                session.add(created_user)
                await session.commit()
                return UserRecord(
                    id=created_user.id,
                    email=email,
                    is_admin=created_user.is_admin
                )
            return user
