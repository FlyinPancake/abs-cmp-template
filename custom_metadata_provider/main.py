from fastapi import FastAPI
from data import BooksResponse
from search import search_with_cache

app = FastAPI()


@app.get("/search")
async def search(query: str, author: str | None = None) -> BooksResponse:
    """Search for books by title and optionally author"""
    return await search_with_cache(query, author)
