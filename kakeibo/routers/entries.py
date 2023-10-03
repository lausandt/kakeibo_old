from typing import Annotated, Optional, Sequence

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from kakeibo.crud import entryCrud
from kakeibo.dependencies import get_db
from kakeibo.schemas import entry_schema

router = APIRouter(
    prefix="/entries",
    tags=["entries"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/entries/{id}",
    status_code=200,
    response_model=entry_schema.Entry,
    response_model_exclude={"owner_id"},
)
async def fetch_entry(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    db: Session = Depends(get_db),
) -> entry_schema.Entry:
    """Search for entries by ID"""
    result = entryCrud.get_entry(db, id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Entry with ID {id} not found")
    return result


@router.get("/search/", status_code=200, response_model=list[entry_schema.Entry])
async def search_entries_with_keyword(
    *,
    db: Session = Depends(get_db),
    keyword: Optional[str] = Query(
        None, min_length=3, examples="daily shopping"  # type:ignore
    ),
) -> Sequence[entry_schema.Entry]:
    """
    Search for entries based on description keyword
    """
    if keyword:
        return entryCrud.get_entry_by_keyword(db=db, keyword=keyword)
    else:
        return entryCrud.get_entries(db)


@router.get("/show_entries", status_code=200, response_model=list[entry_schema.Entry])
async def show_entries(db: Session = Depends(get_db)) -> Sequence[entry_schema.Entry]:
    """Show all the entries in the database"""
    return entryCrud.get_entries(db)
