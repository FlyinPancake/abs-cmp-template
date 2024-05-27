from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, relationship

from .database import Base

search__books = Table(
    "search__books",
    Base.metadata,
    Column("search_results_id", ForeignKey("search_results.id"), primary_key=True),
    Column("books_id", ForeignKey("books.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    datasource_id = Column(
        String, unique=True, nullable=False, index=True
    )  # This is the unique identifier for the book from the data source i.e.: ASIN, or site specific ID
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    author = Column(String, nullable=True)
    narrator = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    published_year = Column(String, nullable=True)

    description = Column(String, nullable=True)
    cover = Column(String, nullable=True)
    isbn = Column(String, nullable=True)
    asin = Column(String, nullable=True)
    genres = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    language = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    series = Column(JSON, nullable=True)

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))


class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True)
    query = Column(String, nullable=False, index=True)
    author = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    matches: Mapped[list["Book"]] = relationship(secondary=search__books)
