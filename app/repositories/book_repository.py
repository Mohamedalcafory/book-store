from typing import Optional, Tuple, List

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
        return Book.query.order_by(Book.id.asc()).all()

    def update(self, book: Book) -> Book:
        db.session.commit()
        db.session.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        db.session.delete(book)
        db.session.commit()
    
    def get_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Book], int]:
        query = Book.query
        if author_id:
            query = query.filter(Book.author_id == author_id)
        if category_id:
            query = query.filter(Book.category_id == category_id)
        if search:
            query = query.filter(Book.title.ilike(f"%{search}%"))
        response = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False,
            count=True
        )
        return response, response.total



