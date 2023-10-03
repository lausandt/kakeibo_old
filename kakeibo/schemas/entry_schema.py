from enum import Enum
from typing import Sequence

from pydantic import BaseModel, Field  # HttpUrl not supported by sqlite


class Period(str, Enum):
    daily: str = "Daily"
    weekly: str = "Weekly"
    monthly: str = "Monthly"
    quarterly: str = "Quarterly"
    yearly: str = "Yearly"


class EntryBase(BaseModel):
    title: str
    amount: int | float = Field(gt=0, description="The amount must be greater than 0")
    description: str = Field(title="The description of the item", max_length=300)
    period: Period | None
    url: str | None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Utilities Water",
                    "amount": 35.4,
                    "description": "water usage bill",
                    "period": "Monthly",
                    "url": "waternet.nl",
                }
            ]
        }
    }


class EntryCreate(EntryBase):
    ...


class Entry(EntryBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class EntriesSearchResults(BaseModel):
    results: Sequence[Entry]
