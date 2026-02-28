from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Many-to-many table
book_category = Table(
    "book_category",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    bio = Column(String)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    isbn = Column(String)
    publication_year = Column(Integer)

    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
    categories = relationship("Category", secondary=book_category)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    books = relationship("Book", secondary=book_category)
