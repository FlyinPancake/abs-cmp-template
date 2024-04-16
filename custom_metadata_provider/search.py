import datetime
from pprint import pprint

from data import BookMetadata, BooksResponse, Series
from models import Book, SearchResult
from pydantic_extra_types.isbn import ISBN
from sqlalchemy import text
from sqlalchemy.orm import Session


async def _search(
    query: str, author: str | None = None
) -> list[tuple[str, BookMetadata]]:
    """
    Search for books by title and optionally author
    return: list of tuples containing the unique identifier for the book from the data source i.e.: ASIN, or site specific ID and the BookMetadata object
    """
    # This is a placeholder for the actual search implementation
    # In a real implementation, this function would search a database or external API
    # for books matching the query and author
    # For this example, we'll just return a single book

    return [
        (
            "name-of-the-wind-1",
            BookMetadata(
                title="The Name of the Wind",
                author="Patrick Rothfuss",
                published_year="2007",
                description="I have stolen princesses back from sleeping barrow kings. I burned down the town of Trebon. I have spent the night with Felurian and left with both my sanity and my life. I was expelled from the University at a younger age than most people are allowed in. I tread paths by moonlight that others fear to speak of during day. I have talked to",
                cover="https://m.media-amazon.com/images/G/02/apparel/rcxgs/tile._CB483369956_.gif",
                isbn="978-3-16-148410-0",
                asin="B07D2CJL5V",
                genres=["Fantasy", "Historical Fiction"],
                tags=["magic", "historical"],
                series=[Series(series="The Kingkiller Chronicle", sequence=1)],
                language="English",
                duration=123456,
                narrator="Nick Podehl",
                subtitle="The Kingkiller Chronicle, Book 1",
                publisher="DAW Books",
            ),
        )
    ]


async def search_with_cache(
    db: Session,
    query: str,
    author: str | None = None,
) -> BooksResponse:
    """Search for books by title and optionally author with caching"""
    # Check if the search result is already in the cache
    cached_search_result = await _get_cached_search_result(db, query, author)
    # If it is, return the cached result
    if cached_search_result:
        return cached_search_result
    # Otherwise, perform the search and cache the result
    search_result = await _search(query, author)
    await _cache_search_result(db, query, author, search_result)
    books = [book for _, book in search_result]
    return BooksResponse(matches=books)


async def _cache_search_result(
    db: Session,
    query: str,
    author: str | None,
    search_result: list[tuple[str, BookMetadata]],
) -> None:
    """Cache the search result"""
    # Cache the search result in the database

    dsids = [
        row[0] for row in db.execute(text("SELECT datasource_id FROM books")).fetchall()
    ]
    pprint(dsids)
    books = [
        Book(
            datasource_id=datasource_id,
            title=book.title,
            author=book.author,
            published_year=book.published_year,
            description=book.description,
            cover=book.cover,
            isbn=book.isbn,
            asin=book.asin,
            genres=book.genres,
            tags=book.tags,
            language=book.language,
            duration=book.duration,
            narrator=book.narrator,
            subtitle=book.subtitle,
            publisher=book.publisher,
            series=[series.model_dump() for series in book.series]
            if book.series
            else [],
        )
        for datasource_id, book in search_result
        if datasource_id not in dsids
    ]

    search_result = SearchResult(query=query, author=author)

    search_result.matches.extend(books)
    db.add(search_result)

    db.commit()


async def _get_cached_search_result(
    db: Session,
    query: str,
    author: str | None,
) -> BooksResponse | None:
    """Get the cached search result"""

    search_result = (
        db.query(SearchResult)
        .filter(SearchResult.query == query)
        .filter(SearchResult.author == author)
        .first()
    )

    if search_result:
        created_at: datetime.datetime = search_result.created_at  # type: ignore
        if (datetime.datetime.now() - created_at) > datetime.timedelta(days=1):
            db.delete(search_result)
            db.commit()
            return None
        return BooksResponse(matches=search_result.matches)  # type: ignore

    return None
