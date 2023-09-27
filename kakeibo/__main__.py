from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from kakeibo.crud import crud
from kakeibo.db.database import SessionLocal, engine
from kakeibo.entry_data import ENTRIES
from kakeibo.models import models
from kakeibo.schemas import schemas
from kakeibo.schemas.schemas import Entry

models.Base.metadata.create_all(bind=engine)

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="kakeibo API", openapi_url="/openapi.json")
api_router = APIRouter()


@api_router.get("/", status_code=200)
def root(request: Request) -> Any:
    """
    Root Get
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "ENTRIES": ENTRIES},
    )


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/entries/", response_model=schemas.Entry)
def create_item_for_user(
    user_id: int, entry: schemas.EntryCreate, db: Session = Depends(get_db)
):
    return crud.create_user_entry(db=db, entry=entry, user_id=user_id)


@api_router.get("/entries/{id}", status_code=200, response_model=schemas.Entry)
def fetch_entry(*, id: int, db: Session = Depends(get_db)) -> dict:
    """
    Fetch a single entry by ID
    """
    result = crud.get_entry(db=db, id=id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Entry with ID {id} not found")
    return result


@api_router.get("/search/{keyword}", status_code=200, response_model=list[Entry])
def search_entries_with_keyword(
    *,
    db: Session = Depends(get_db),
    keyword: Optional[str] = Query(
        None, min_length=3, examples="daily shopping"  # type:ignore
    ),
) -> list[Entry]:
    """
    Search for entries based on description keyword
    """
    if keyword:
        return crud.get_entry_by_keyword(db=db, keyword=keyword)
    else:
        return crud.get_entries(db)


@api_router.get("/search", status_code=200, response_model=list[Entry])
def search_entries(db: Session = Depends(get_db)) -> list[Entry]:
    """See all the entries"""
    return crud.get_entries(db)


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
