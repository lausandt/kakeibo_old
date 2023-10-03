from typing import Any, Sequence

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column
from sqlalchemy.orm import Session

from kakeibo.models.models import User
from kakeibo.schemas import user_schema


def get_user(db: Session, *, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, *, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Sequence[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate) -> User:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(
        email=user.email, name=user.name, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def is_super_user(user: User) -> Column[bool]:
    return user.is_super_user


def update(db: Session, *, user: User, key: str, value: str | bool) -> User:
    obj_data = jsonable_encoder(user)
    for field in obj_data:
        if field == key:
            setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def remove(db: Session, *, id: int) -> Any | None:
    obj = db.query(User).get(id)
    db.delete(obj)
    db.commit()
    return obj
