from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    success: bool


class User(UserBase):
    id: UUID
    is_admin: bool

    class Config:
        from_attributes = True
