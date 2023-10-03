from typing import Sequence

from pydantic import BaseModel, EmailStr  # HttpUrl not supported by sqlite

from . import entry_schema


class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_active: bool = True
    is_super_user: bool = False


class UserUpdate(UserBase):
    ...


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    items: list[entry_schema.Entry] = []

    class Config:
        from_attributes = True
