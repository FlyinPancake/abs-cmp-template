import logging
import sys

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import database, models
from .data import BooksResponse
from .search import search_with_cache

models.Base.metadata.create_all(bind=database.sqla_engine)


app = FastAPI()

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/search")
async def search(
    query: str,
    author: str | None = None,
    db: Session = Depends(get_db),
) -> BooksResponse:
    """Search for books by title and optionally author"""
    return await search_with_cache(db, query, author)
