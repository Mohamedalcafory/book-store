from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import date
from typing import Optional


class BookCreateSchema(Schema):
    """Schema for creating a new book"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True, validate=validate.Length(max=1000))
    release_date = fields.Date(allow_none=True)
    price = fields.Float(allow_none=True, validate=validate.Range(min=0))
    author_id = fields.Int(required=True, validate=validate.Range(min=1))
    category_id = fields.Int(required=True, validate=validate.Range(min=1))
    stock = fields.Int(validate=validate.Range(min=0))
    creator = fields.Str(validate=validate.Length(max=120))

    @validates_schema
    def validate_release_date(self, data, **kwargs):
        """Validate release date is not in the future"""
        if data.get('release_date') and data['release_date'] > date.today():
            raise ValidationError('Release date cannot be in the future', 'release_date')


class BookUpdateSchema(Schema):
    """Schema for updating a book"""
    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True, validate=validate.Length(max=1000))
    release_date = fields.Date(allow_none=True)
    price = fields.Float(allow_none=True, validate=validate.Range(min=0))
    author_id = fields.Int(validate=validate.Range(min=1))
    category_id = fields.Int(validate=validate.Range(min=1))
    stock = fields.Int(validate=validate.Range(min=0))
    creator = fields.Str(validate=validate.Length(max=120))

    @validates_schema
    def validate_release_date(self, data, **kwargs):
        """Validate release date is not in the future"""
        if data.get('release_date') and data['release_date'] > date.today():
            raise ValidationError('Release date cannot be in the future', 'release_date')


class BookResponseSchema(Schema):
    """Schema for book response serialization"""
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    release_date = fields.Date()
    price = fields.Float()
    author_id = fields.Int()
    category_id = fields.Int()
    stock = fields.Int()
    creator = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
    # Include related data
    author_name = fields.Method('get_author_name')
    category_name = fields.Method('get_category_name')

    def get_author_name(self, obj):
        """Get author name from related author object"""
        if hasattr(obj, 'author') and obj.author:
            return obj.author.name
        return None

    def get_category_name(self, obj):
        """Get category name from related category object"""
        if hasattr(obj, 'category') and obj.category:
            return obj.category.name
        return None


class BookListResponseSchema(Schema):
    """Schema for paginated book list response"""
    books = fields.Nested(BookResponseSchema, many=True)
    pagination = fields.Dict(keys=fields.Str(), values=fields.Raw())


class BookSearchSchema(Schema):
    """Schema for book search parameters"""
    query = fields.Str(validate=validate.Length(min=1, max=100))
    author_id = fields.Int(validate=validate.Range(min=1))
    category_id = fields.Int(validate=validate.Range(min=1))
    page = fields.Int(validate=validate.Range(min=1))
    per_page = fields.Int(validate=validate.Range(min=1, max=100))
