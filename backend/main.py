from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .database import create_db_and_tables, get_session
from .models import Book, BookCreate, BookUpdate, BookResponse, User, UserCreate, Token
from .auth import authenticate_user, create_access_token, get_current_user, get_password_hash

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")

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
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
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

@app.post("/register", response_model=User)
def register(user: UserCreate, session: SessionDep):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user