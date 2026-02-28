from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, schemas, crud
from auth_middleware import auth_middleware
from database import engine, SessionLocal, Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.middleware("http")(auth_middleware)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/")
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    new_author = models.Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@app.get("/authors/")
def read_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)


@app.put("/authors/{author_id}")
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.update_author(db, author_id, author)


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.delete_author(db, author_id)


@app.post("/categories/")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@app.get("/categories/")
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.post("/books/")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/")
def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.put("/books/{book_id}")
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)


@app.get("/books/filter/")
def filter_books(
    author_id: int = None,
    category_id: int = None,
    year: int = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_books_filtered(db, author_id, category_id, year, limit)


@app.get("/stats/total-books")
def total_books(db: Session = Depends(get_db)):
    return crud.get_total_books(db)


@app.get("/stats/average-year")
def average_year(db: Session = Depends(get_db)):
    return crud.get_average_year(db)


@app.get("/stats/books-per-author")
def books_per_author(db: Session = Depends(get_db)):
    return crud.books_per_author(db)


@app.get("/stats/books-per-category")
def books_per_category(db: Session = Depends(get_db)):
    return crud.books_per_category(db)


@app.get("/stats/authors-with-books")
def authors_with_books(db: Session = Depends(get_db)):
    return crud.authors_with_books(db)

# OPTIONAL PART

# @app.get("/books/insights")
# def books_insights(db: Session = Depends(get_db)):

#     books = db.query(models.Book).all()

#     if not books:
#         return {
#             "top_authors": [],
#             "busy_years": {}
#         }


#     valid_books = []
#     for book in books:
#         if (
#             book.author is not None
#             and book.publication_year is not None
#             and 1900 <= book.publication_year <= 2100
#         ):
#             valid_books.append(book)

#     if not valid_books:
#         return {
#             "top_authors": [],
#             "busy_years": {}
#         }

#     author_counts = {}
#     for book in valid_books:
#         author_name = book.author.name
#         author_counts[author_name] = author_counts.get(author_name, 0) + 1

#     top_authors = sorted(
#         author_counts.items(),
#         key=lambda x: x[1],
#         reverse=True
#     )[:5]

#     top_authors_result = [
#         {"author": name, "book_count": count}
#         for name, count in top_authors
#     ]

#     year_map = {}
#     for book in valid_books:
#         year = book.publication_year
#         year_map.setdefault(year, []).append(book.title)

#     busy_years = {
#         year: titles
#         for year, titles in sorted(year_map.items())
#         if len(titles) >= 2
#     }


#     return {
#         "top_authors": top_authors_result,
#         "busy_years": busy_years
#     }
