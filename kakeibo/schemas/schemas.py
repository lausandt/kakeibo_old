from enum import Enum
from typing import Sequence

from pydantic import BaseModel  # HttpUrl not supported by sqlite


class Period(str, Enum):
    daily: str = "Daily"
    weekly: str = "Weekly"
    monthly: str = "Monthly"
    quarterly: str = "Quarterly"
    yearly: str = "Yearly"


class EntryBase(BaseModel):
    title: str
    amount: int | float
    description: str
    period: Period | None
    url: str | None


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class EntriesSearchResults(BaseModel):
    results: Sequence[Entry]


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_super_user: bool
    items: list[Entry] = []

    class Config:
        from_attributes = True
