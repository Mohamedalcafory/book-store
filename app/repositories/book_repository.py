from typing import Optional

from app import db
from app.models.book import Book


class BookRepository:
    def add(self, book: Book) -> Book:
        db.session.add(book)
        db.session.commit()
        db.session.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return db.session.get(Book, book_id)

    def list_all(self) -> list[Book]:
        print("BookRepository")
        books = Book.query.all()
        return books
        # print(Book.query.order_by(Book.id.asc()).all())
        # return Book.query.order_by(Book.id.asc()).all()

    def update(self, book: Book) -> Book:
        db.session.commit()
        db.session.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        db.session.delete(book)
        db.session.commit()


