from typing import Optional
from pydantic import BaseModel, Field

class Series(BaseModel):
    series: str = Field(..., description="The name of the series", examples=["The Poppy War", "The Empyrean"])
    sequence: int | None  = Field(None, description="The sequence of the book in the series", examples=[1, 2])


class BookMetadata(BaseModel):
    title: str = Field(..., description="The title of the book", examples=["Babel", "Fourth Wing"])
    subtitle: Optional[str] = Field(None, description="The subtitle of the book", examples=["Or the Necessity of Violence: An Arcane History of The Oxford Translators' Revolution", None])
    author: str | None = Field(None, description="The author of the book", examples=["R. F. Kuang", "Rebecca Yarros"])
    narrator: str | None = Field(None, description="The narrator of the book", examples=["Emily Woo Zeller", "Carly Robins"])
    publisher: str | None = Field(None, description="The publisher of the book", examples=["Harper Voyager", "Entangled: Amara"])
    publishedYear: str | None = Field(None, description="The year the book was published", examples=["2020", "2019"])
    description: str | None = Field(None, description="The description of the book", examples=["Traduttore, traditore: An act of translation is always an act of betrayal.\nOxford, 1836\nThe city of dreaming spires."])
    cover: str | None = Field(None, description="The URL of the book cover", examples=["https://m.media-amazon.com/images/G/02/apparel/rcxgs/tile._CB483369956_.gif"])
    isbn: str | None = Field(None, description="The ISBN of the book", examples=["9780062662619", "9781640637267"])
    asin: str | None = Field(None, description="The ASIN of the book", examples=["B07D2CJL5V", "B07V7W9KJ8"])
    genres: list[str] | None = Field(None, description="The genres of the book", examples=[["Fantasy", "Historical Fiction"], ["Romance", "Contemporary Romance"]])
    tags: list[str] | None = Field(None, description="The tags of the book", examples=[["magic", "historical"], ["military", "contemporary"]])
    series: list[Series] | None = Field(None, description="The series of the book", examples=[[], [{"series": "The Empyrean", "sequence": 1}]])
    language: str | None = Field(None, description="The language of the book", examples=["English", "Spanish"])
    duration: int | None = Field(None, description="The duration of the book in seconds", examples=[123456, 654321])

class BooksResponse(BaseModel):
    matches: list[BookMetadata] = Field(..., description="The list of books that match the search criteria")