from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import date
from typing import Optional


class AuthorCreateSchema(Schema):
    """Schema for creating a new author"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    biography = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    date_of_birth = fields.Date(allow_none=True)
    country = fields.Str(allow_none=True, validate=validate.Length(max=80))

    @validates_schema
    def validate_date_of_birth(self, data, **kwargs):
        """Validate date of birth is not in the future"""
        if data.get('date_of_birth') and data['date_of_birth'] > date.today():
            raise ValidationError('Date of birth cannot be in the future', 'date_of_birth')


class AuthorUpdateSchema(Schema):
    """Schema for updating an author"""
    name = fields.Str(validate=validate.Length(min=1, max=120))
    biography = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    date_of_birth = fields.Date(allow_none=True)
    country = fields.Str(allow_none=True, validate=validate.Length(max=80))

    @validates_schema
    def validate_date_of_birth(self, data, **kwargs):
        """Validate date of birth is not in the future"""
        if data.get('date_of_birth') and data['date_of_birth'] > date.today():
            raise ValidationError('Date of birth cannot be in the future', 'date_of_birth')


class AuthorResponseSchema(Schema):
    """Schema for author response serialization"""
    id = fields.Int()
    name = fields.Str()
    biography = fields.Str()
    date_of_birth = fields.Date()
    country = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
    # Include related data
    books_count = fields.Method('get_books_count')

    def get_books_count(self, obj):
        """Get number of books by this author"""
        if hasattr(obj, 'books') and obj.books:
            return len(obj.books)
        return 0


class AuthorListResponseSchema(Schema):
    """Schema for paginated author list response"""
    authors = fields.Nested(AuthorResponseSchema, many=True)
    pagination = fields.Dict(keys=fields.Str(), values=fields.Raw())


class AuthorSearchSchema(Schema):
    """Schema for author search parameters"""
    query = fields.Str(validate=validate.Length(min=1, max=100))
    country = fields.Str(validate=validate.Length(max=80))
    page = fields.Int(validate=validate.Range(min=1))
    per_page = fields.Int(validate=validate.Range(min=1, max=100))
