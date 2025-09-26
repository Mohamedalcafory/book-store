from typing import Optional, List, Tuple
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schemas import CategoryCreateSchema, CategoryUpdateSchema


class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    def create_category(self, data: dict) -> Category:
        """Create a new category"""
        # Validate data using schema
        schema = CategoryCreateSchema()
        validated_data = schema.load(data)
        
        # Check if category with same name already exists
        existing_category = self.repository.get_by_name(validated_data['name'])
        if existing_category:
            raise ValueError(f"Category with name '{validated_data['name']}' already exists")
        
        # Create new category
        category = Category(**validated_data)
        return self.repository.add(category)

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return self.repository.get_by_id(category_id)

    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Get category by name"""
        return self.repository.get_by_name(name)

    def get_categories_paginated(self, page: int = 1, per_page: int = 10, 
                                search: Optional[str] = None) -> Tuple[List[Category], int]:
        """Get paginated list of categories with optional filtering"""
        from app import db
        
        query = Category.query
        
        # Apply search filter
        if search:
            query = query.filter(Category.name.ilike(f'%{search}%'))
        
        # Order by name
        query = query.order_by(Category.name.asc())
        
        # Get paginated results
        paginated_categories = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return paginated_categories, paginated_categories.total

    def list_all_categories(self) -> List[Category]:
        """Get all categories"""
        return self.repository.list_all()

    def update_category(self, category_id: int, data: dict) -> Optional[Category]:
        """Update a category"""
        category = self.repository.get_by_id(category_id)
        if not category:
            return None
        
        # Validate data using schema
        schema = CategoryUpdateSchema()
        validated_data = schema.load(data)
        
        # Check if name is being changed and if new name already exists
        if 'name' in validated_data and validated_data['name'] != category.name:
            existing_category = self.repository.get_by_name(validated_data['name'])
            if existing_category and existing_category.id != category_id:
                raise ValueError(f"Category with name '{validated_data['name']}' already exists")
        
        # Update category fields
        for field, value in validated_data.items():
            setattr(category, field, value)
        
        return self.repository.update(category)

    def delete_category(self, category_id: int) -> bool:
        """Delete a category"""
        category = self.repository.get_by_id(category_id)
        if not category:
            return False
        
        # Check if category has books
        if category.books:
            raise ValueError("Cannot delete category with existing books. Please remove all books first.")
        
        self.repository.delete(category)
        return True


# Create service instance
category_service = CategoryService()
