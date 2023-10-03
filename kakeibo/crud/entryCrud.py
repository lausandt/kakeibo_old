from typing import Sequence

from sqlalchemy.orm import Session

from kakeibo.models.models import Entry
from kakeibo.schemas import entry_schema


def get_entry(db: Session, id: int) -> Entry | None:
    return db.query(Entry).filter(Entry.id == id).first()


def get_entry_by_keyword(db: Session, keyword: str) -> Sequence[Entry]:
    result = db.query(Entry).filter(Entry.description.contains(keyword)).all()
    return result


def get_entries(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Entry]:
    return db.query(Entry).offset(skip).limit(limit).all()


def create_user_entry(
    db: Session, entry: entry_schema.EntryCreate, user_id: int
) -> Entry:
    db_entry = Entry(**entry.model_dump(), owner_id=user_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
