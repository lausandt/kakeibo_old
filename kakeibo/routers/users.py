from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from kakeibo.crud import entryCrud
from kakeibo.crud.userCRUD import *
from kakeibo.dependencies import get_db
from kakeibo.schemas import entry_schema, user_schema

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"email": "Not found"}},
)


@router.post("/users/", response_model=user_schema.User)
async def user_create(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@router.get("/users/", response_model=list[user_schema.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/{user_id}/superuser")
async def is_superuser(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user:
        return is_super_user(db_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put(
    "/users/{user_id}/update_user",
    response_model=user_schema.UserUpdate,
    response_model_exclude={"name"},
)
async def update_user(
    user_id: int, key: str, value: Any, db: Session = Depends(get_db)
):
    valid_updates = ["email", "is_active", "is_superuser"]
    if key in valid_updates:
        db_user = get_user(db, user_id=user_id)
        if db_user:
            if value.lower() == "true":
                value = bool(value)
            return update(db, user=db_user, key=key, value=value)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(
            status_code=418,
            detail="You can only update email, if use is active or if super user",
        )


@router.post("/users/{user_id}/entries/", response_model=entry_schema.Entry)
async def create_entry_for_user(
    user_id: int, entry: entry_schema.EntryCreate, db: Session = Depends(get_db)
):
    return entryCrud.create_user_entry(db=db, entry=entry, user_id=user_id)


@router.delete("/users/{user_id}/delete_user")
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    return remove(db, id=user_id)
