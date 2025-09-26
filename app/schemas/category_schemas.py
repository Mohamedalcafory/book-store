from marshmallow import Schema, fields, validate
from typing import Optional


class CategoryCreateSchema(Schema):
    """Schema for creating a new category"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    description = fields.Str(allow_none=True, validate=validate.Length(max=1000))


class CategoryUpdateSchema(Schema):
    """Schema for updating a category"""
    name = fields.Str(validate=validate.Length(min=1, max=120))
    description = fields.Str(allow_none=True, validate=validate.Length(max=1000))


class CategoryResponseSchema(Schema):
    """Schema for category response serialization"""
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
    # Include related data
    books_count = fields.Method('get_books_count')

    def get_books_count(self, obj):
        """Get number of books in this category"""
        if hasattr(obj, 'books') and obj.books:
            return len(obj.books)
        return 0


class CategoryListResponseSchema(Schema):
    """Schema for paginated category list response"""
    categories = fields.Nested(CategoryResponseSchema, many=True)
    pagination = fields.Dict(keys=fields.Str(), values=fields.Raw())


class CategorySearchSchema(Schema):
    """Schema for category search parameters"""
    query = fields.Str(validate=validate.Length(min=1, max=100))
    page = fields.Int(validate=validate.Range(min=1))
    per_page = fields.Int(validate=validate.Range(min=1, max=100))
