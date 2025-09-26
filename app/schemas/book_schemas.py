from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import date
from typing import Optional


class BookCreateSchema(Schema):
    """Schema for creating a new book"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(allow_none=True, validate=validate.Length(max=1000))
    release_date = fields.Date(allow_none=True)
    price = fields.Float(allow_none=True, validate=validate.Range(min=0))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=100))
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
    author = fields.Str(validate=validate.Length(min=1, max=200))
    category = fields.Str(validate=validate.Length(min=1, max=100))
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
    author = fields.Str()
    category = fields.Str()
    stock = fields.Int()
    creator = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class BookListResponseSchema(Schema):
    """Schema for paginated book list response"""
    books = fields.Nested(BookResponseSchema, many=True)
    pagination = fields.Dict(keys=fields.Str(), values=fields.Raw())


class BookSearchSchema(Schema):
    """Schema for book search parameters"""
    query = fields.Str(validate=validate.Length(min=1, max=100))
    author = fields.Str(validate=validate.Length(min=1, max=200))
    category = fields.Str(validate=validate.Length(min=1, max=100))
    page = fields.Int(validate=validate.Range(min=1))
    per_page = fields.Int(validate=validate.Range(min=1, max=100))
