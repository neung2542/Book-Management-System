from sqlmodel import SQLModel, Field
from datetime import datetime

class BookBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    published_year: int | None = Field(default=None, ge=1000, le=2024)
    genre: str | None = Field(default=None, max_length=100)

class Book(BookBase, table=True):
    __tablename__ = "books"
    
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)

class BookCreate(BookBase):
    pass

class BookUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=255)
    published_year: int | None = Field(default=None, ge=1000, le=2024)
    genre: str | None = Field(default=None, max_length=100)

class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime