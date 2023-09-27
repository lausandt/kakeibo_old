"""
By creating functions that are only dedicated to interacting with the database (get a user or an item)
independent of your path operation function, you can more easily reuse them in multiple parts and also add unit tests for them.
"""
from typing import Any

from sqlalchemy.orm import Session

from kakeibo.models import models
from kakeibo.schemas import schemas


def get_user(db: Session, user_id: int) -> Any:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Any:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Any:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> Any:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_entry(db: Session, id: int) -> Any:
    return db.query(models.Entry).filter(models.Entry.id == id).first()


def get_entry_by_keyword(db: Session, keyword: str) -> Any:
    result = (
        db.query(models.Entry).filter(models.Entry.description.contains(keyword)).all()
    )
    return result


def get_entries(db: Session, skip: int = 0, limit: int = 100) -> Any:
    return db.query(models.Entry).offset(skip).limit(limit).all()


def create_user_entry(db: Session, entry: schemas.EntryCreate, user_id: int) -> Any:
    db_entry = models.Entry(
        **entry.model_dump(), owner_id=user_id
    )  # perhaps model_dump() instead of dict
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
