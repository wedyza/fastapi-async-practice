from uuid import UUID

from sqlalchemy import Boolean, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.postgresql.models.base import Base


class UsersOrm(Base):
    __tablename__: str = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
