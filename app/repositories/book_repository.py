from typing import Optional, Tuple, List
from datetime import date

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
        author: Optional[str] = None,
        category: Optional[str] = None,
        price: Optional[float] = None,
        release_date: Optional[date] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Book], int]:
        query = Book.query
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if category:
            query = query.filter(Book.category.ilike(f"%{category}%"))
        if price:
            query = query.filter(Book.price == price)
        if release_date:
            query = query.filter(Book.release_date == release_date)
        if search:
            query = query.filter(
                Book.title.ilike(f"%{search}%") |
                Book.description.ilike(f"%{search}%") |
                Book.author.ilike(f"%{search}%") |
                Book.category.ilike(f"%{search}%")
            )
        response = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False,
            count=True
        )
        return response, response.total



