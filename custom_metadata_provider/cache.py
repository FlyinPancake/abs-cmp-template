from data import BooksResponse


async def search(query: str, author: str | None = None) -> BooksResponse:
    """Search for books by title and optionally author"""
    return {"Hello": "World"}