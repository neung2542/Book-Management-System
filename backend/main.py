from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


class BookBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    published_year: int | None = Field(default=None, ge=1000, le=2024)
    genre: str | None = Field(default=None, max_length=100)

class Book(BookBase, table=True):
    
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

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Books CRUD API with SQLModel"}

@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, session: SessionDep):
        db_book = Book.model_validate(book)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book
    

@app.get("/books/", response_model=list[BookResponse])
def read_books(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: Annotated[int, Query(le=100)] = 100,
):
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.patch("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.model_dump(exclude_unset=True)
    book_db.sqlmodel_update(book_data)
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    return book_db

@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book_db)
    session.commit()
    return {"ok": True}