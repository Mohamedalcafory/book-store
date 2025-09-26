from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from typing import Dict, Any

from flask import Blueprint

from app.services.book_service import book_service
from app.schemas.book_schemas import BookCreateSchema, BookUpdateSchema, BookResponseSchema

# Create namespace for Swagger documentation
book_ns = Namespace('books', description='Book operations')


book_create_model = book_ns.model(
    "BookCreate",
    {
        "title": fields.String(required=True),
        "description": fields.String,
        "price": fields.Float(required=True),
        "release_date": fields.String(description="YYYY-MM-DD"),
        "author": fields.String(required=True),
        "category": fields.String(required=True),
        "stock": fields.Integer(required=True),
        "creator": fields.String(required=True),
    },
)

book_update_model = book_ns.model(
    "BookUpdate",
    {
        "title": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "release_date": fields.String(description="YYYY-MM-DD"),
        "author": fields.String,
        "category": fields.String,
        "stock": fields.Integer,
        "creator": fields.String,
    },
)

book_model = book_ns.model(
    "Book",
    {
        "id": fields.Integer(readOnly=True),
        "title": fields.String(required=True),
        "description": fields.String,
        "release_date": fields.String(description="YYYY-MM-DD"),
        "price": fields.Float,
        "author": fields.String(required=True),
        "category": fields.String(required=True),
        "stock": fields.Integer,
        "creator": fields.String,
    },
)

pagination_model = book_ns.model(
    "Pagination",
    {
        "page": fields.Integer,
        "per_page": fields.Integer,
        "total": fields.Integer,
        "pages": fields.Integer,
        "has_next": fields.Boolean,
        "has_prev": fields.Boolean,
        "next_num": fields.Integer,
        "prev_num": fields.Integer,
    },
)

book_list_model = book_ns.model(
    "BookList",
    {
        "books": fields.Nested(book_model, many=True),
        "pagination": fields.Nested(pagination_model),
    },
)
@book_ns.route('')
class BookList(Resource):
    @book_ns.doc('create_book')  # Documents this endpoint in Swagger UI with the name 'create_book'
    @book_ns.expect(book_create_model)  # Specifies that this endpoint expects a request body matching book_create_model
    @book_ns.marshal_with(book_model, code=201)  # Serializes the response using book_model and sets 201 status code
    @book_ns.response(400, 'Validation Error')  # Documents that this endpoint may return a 400 error
    @book_ns.response(401, 'Authentication required')  # Documents that this endpoint requires authentication
    @book_ns.response(500, 'Internal Server Error')  # Documents that this endpoint may return a 500 error
    
    @jwt_required()
    def post(self):
        """Create a new book"""
        try:
            data = request.get_json()
            # Validate with existing Marshmallow schema
            schema = BookCreateSchema()
            validated_data = schema.load(data)
            
            book = book_service.create_book(validated_data)
            return BookResponseSchema().dump(book), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to create book'}, 500

    @book_ns.doc('list_books')  # Documents this endpoint in Swagger UI with the name 'list_books'
    @book_ns.marshal_with(book_list_model)  # Serializes the response using book_list_model
    @book_ns.response(401, 'Authentication required')  # Documents that this endpoint requires authentication
    @book_ns.response(500, 'Internal Server Error')  # Documents that this endpoint may return a 500 error
    @book_ns.param('page', 'Page number', type=int, default=1)
    @book_ns.param('per_page', 'Items per page (max 100)', type=int, default=10)
    @book_ns.param('author', 'Filter by author name', type=str)
    @book_ns.param('category', 'Filter by category name', type=str)
    @book_ns.param('search', 'Search books by title', type=str)
    @jwt_required()
    def get(self):
        """List books with optional filtering and pagination"""
        try:
            print("get books")
            # Extract query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            author = request.args.get('author', type=str)
            category = request.args.get('category', type=str)
            search = request.args.get('search', type=str)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:
                per_page = 10
                
            books, total = book_service.get_books_paginated(
                page=page,
                per_page=per_page,
                author=author,
                category=category,
                search=search
            )
            schema = BookResponseSchema(many=True)
            return {
                'books': schema.dump(books),
                'pagination': {
                    'page': books.page,
                    'per_page': books.per_page,
                    'total': total,
                    'pages': books.pages,
                    'has_next': books.has_next,
                    'has_prev': books.has_prev,
                    'next_num': books.next_num,
                    'prev_num': books.prev_num,
                }
            }
        except Exception as e:
            print(f"Error in {book_ns.name} namespace:", e)
            return {'error': 'Failed to retrieve books'}, 500


@book_ns.route('/<int:book_id>')
@book_ns.param('book_id', 'The book identifier', type=int)
class Book(Resource):
    @book_ns.doc('get_book')  # Documents this endpoint in Swagger UI with the name 'get_book'
    @book_ns.marshal_with(book_model)  # Serializes the response using book_model
    @book_ns.response(401, 'Authentication required')  # Documents that this endpoint requires authentication
    @book_ns.response(404, 'Book not found')  # Documents that this endpoint may return a 404 error
    @book_ns.response(500, 'Internal Server Error')  # Documents that this endpoint may return a 500 error
    @jwt_required()
    def get(self, book_id):
        """Get specific book details"""
        try:
            book = book_service.get_book_by_id(book_id)
            if not book:
                return {'error': 'Book not found'}, 404
            return BookResponseSchema().dump(book)
        except Exception as e:
            return {'error': 'Failed to retrieve book'}, 500

    @book_ns.doc('update_book')  # Documents this endpoint in Swagger UI with the name 'update_book'
    @book_ns.expect(book_update_model)  # Specifies that this endpoint expects a request body matching book_update_model
    @book_ns.marshal_with(book_model)  # Serializes the response using book_model
    @book_ns.response(400, 'Validation Error')  # Documents that this endpoint may return a 400 error
    @book_ns.response(401, 'Authentication required')  # Documents that this endpoint requires authentication
    @book_ns.response(404, 'Book not found')  # Documents that this endpoint may return a 404 error
    @book_ns.response(500, 'Internal Server Error')  # Documents that this endpoint may return a 500 error
    @jwt_required()
    def patch(self, book_id):
        """Update book details"""
        try:
            data = request.get_json()
            # Validate with existing Marshmallow schema
            schema = BookUpdateSchema()
            validated_data = schema.load(data)
            
            book = book_service.update_book(book_id, validated_data)
            if not book:
                return {'error': 'Book not found'}, 404
            schema = BookResponseSchema()
            return schema.dump(book)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to update book'}, 500