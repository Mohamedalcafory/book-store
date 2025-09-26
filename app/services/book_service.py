from typing import List, Tuple, Optional
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.category_repository import CategoryRepository


class BookService:
    def __init__(self):
        self.book_repository = BookRepository()
        self.author_repository = AuthorRepository()
        self.category_repository = CategoryRepository()

    def create_book(self, data: dict) -> Book:
        """Create a new book with validation"""
        # Validate author exists
        author = self.author_repository.get_by_id(data.get('author_id'))
        if not author:
            raise ValueError("Author not found")
        
        # Validate category exists
        category = self.category_repository.get_by_id(data.get('category_id'))
        if not category:
            raise ValueError("Category not found")
        
        # Create book instance
        book = Book(
            title=data['title'],
            description=data.get('description'),
            release_date=data.get('release_date'),
            price=data.get('price'),
            author_id=data['author_id'],
            category_id=data['category_id'],
            stock=data.get('stock', 0),
            creator=data.get('creator', 'System')
        )
        
        return self.book_repository.add(book)

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Get a book by ID"""
        return self.book_repository.get_by_id(book_id)

    def get_books_paginated(
        self, 
        page: int = 1, 
        per_page: int = 10,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Book], int]:
        """Get paginated books with optional filtering"""
        # This would typically use a more sophisticated query builder
        # For now, we'll implement basic filtering
        books = self.book_repository.list_all()
        
        # Apply filters
        if author_id:
            books = [book for book in books if book.author_id == author_id]
        
        if category_id:
            books = [book for book in books if book.category_id == category_id]
        
        if search:
            search_lower = search.lower()
            books = [
                book for book in books 
                if search_lower in book.title.lower() or 
                   (book.description and search_lower in book.description.lower())
            ]
        
        # Calculate pagination
        total = len(books)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_books = books[start:end]
        
        return paginated_books, total

    def update_book(self, book_id: int, data: dict) -> Optional[Book]:
        """Update a book with validation"""
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return None
        
        # Validate author if provided
        if 'author_id' in data:
            author = self.author_repository.get_by_id(data['author_id'])
            if not author:
                raise ValueError("Author not found")
        
        # Validate category if provided
        if 'category_id' in data:
            category = self.category_repository.get_by_id(data['category_id'])
            if not category:
                raise ValueError("Category not found")
        
        # Update book fields
        for field, value in data.items():
            if hasattr(book, field) and value is not None:
                setattr(book, field, value)
        
        return self.book_repository.update(book)

    def delete_book(self, book_id: int) -> bool:
        """Delete a book"""
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return False
        
        self.book_repository.delete(book)
        return True

    def get_books_by_author(self, author_id: int) -> List[Book]:
        """Get all books by a specific author"""
        books = self.book_repository.list_all()
        return [book for book in books if book.author_id == author_id]

    def get_books_by_category(self, category_id: int) -> List[Book]:
        """Get all books in a specific category"""
        books = self.book_repository.list_all()
        return [book for book in books if book.category_id == category_id]

    def search_books(self, query: str) -> List[Book]:
        """Search books by title and description"""
        books = self.book_repository.list_all()
        query_lower = query.lower()
        
        return [
            book for book in books
            if query_lower in book.title.lower() or
               (book.description and query_lower in book.description.lower())
        ]
