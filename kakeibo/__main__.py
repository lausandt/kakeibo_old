from pathlib import Path

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request

from .db.database import engine
from .models import models
from .routers import entries, users

# from fastapi.security import OAuth2PasswordBearer


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="kakeibo API", openapi_url="/openapi.json")


@app.get("/", status_code=200)
async def root(request: Request) -> dict:
    """
    Root Get
    """
    return {"message": "The kakeibo app"}


app.include_router(users.router)
app.include_router(entries.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
