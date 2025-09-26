from typing import Optional, List, Tuple
from app.models.author import Author
from app.repositories.author_repository import AuthorRepository
from app.schemas.author_schemas import AuthorCreateSchema, AuthorUpdateSchema


class AuthorService:
    def __init__(self):
        self.repository = AuthorRepository()

    def create_author(self, data: dict) -> Author:
        """Create a new author"""
        # Validate data using schema
        schema = AuthorCreateSchema()
        validated_data = schema.load(data)
        
        # Check if author with same name already exists
        existing_author = self.repository.get_by_name(validated_data['name'])
        if existing_author:
            raise ValueError(f"Author with name '{validated_data['name']}' already exists")
        
        # Create new author
        author = Author(**validated_data)
        return self.repository.add(author)

    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        """Get author by ID"""
        return self.repository.get_by_id(author_id)

    def get_author_by_name(self, name: str) -> Optional[Author]:
        """Get author by name"""
        return self.repository.get_by_name(name)

    def get_authors_paginated(self, page: int = 1, per_page: int = 10, 
                            search: Optional[str] = None, 
                            country: Optional[str] = None) -> Tuple[List[Author], int]:
        """Get paginated list of authors with optional filtering"""
        from app import db
        
        query = Author.query
        
        # Apply search filter
        if search:
            query = query.filter(Author.name.ilike(f'%{search}%'))
        
        # Apply country filter
        if country:
            query = query.filter(Author.country.ilike(f'%{country}%'))
        
        # Order by name
        query = query.order_by(Author.name.asc())
        
        # Get paginated results
        paginated_authors = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return paginated_authors, paginated_authors.total

    def list_all_authors(self) -> List[Author]:
        """Get all authors"""
        return self.repository.list_all()

    def update_author(self, author_id: int, data: dict) -> Optional[Author]:
        """Update an author"""
        author = self.repository.get_by_id(author_id)
        if not author:
            return None
        
        # Validate data using schema
        schema = AuthorUpdateSchema()
        validated_data = schema.load(data)
        
        # Check if name is being changed and if new name already exists
        if 'name' in validated_data and validated_data['name'] != author.name:
            existing_author = self.repository.get_by_name(validated_data['name'])
            if existing_author and existing_author.id != author_id:
                raise ValueError(f"Author with name '{validated_data['name']}' already exists")
        
        # Update author fields
        for field, value in validated_data.items():
            setattr(author, field, value)
        
        return self.repository.update(author)

    def delete_author(self, author_id: int) -> bool:
        """Delete an author"""
        author = self.repository.get_by_id(author_id)
        if not author:
            return False
        
        # Check if author has books
        if author.books:
            raise ValueError("Cannot delete author with existing books. Please remove all books first.")
        
        self.repository.delete(author)
        return True


# Create service instance
author_service = AuthorService()
