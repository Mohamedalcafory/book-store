from flask import request
from flask_restx import Namespace, Resource
from typing import Dict, Any

from app.services.book_service import book_service
from app.schemas.book_schemas import BookCreateSchema, BookUpdateSchema, BookResponseSchema

# Create namespace for Swagger documentation
book_ns = Namespace('books', description='Book operations')


@book_ns.route('')
class BookList(Resource):
    @book_ns.doc('create_book')
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

    @book_ns.doc('list_books')
    def get(self):
        """List books with optional filtering and pagination"""
        try:
            # # Extract query parameters
            # page = request.args.get('page', 1, type=int)
            # per_page = request.args.get('per_page', 10, type=int)
            # author_id = request.args.get('author_id', type=int)
            # category_id = request.args.get('category_id', type=int)
            # search = request.args.get('search', type=str)
            
            # # Validate pagination parameters
            # if page < 1:
            #     page = 1
            # if per_page < 1 or per_page > 100:
            #     per_page = 10
                
            # books, total = BookService.get_books_paginated(
            #     page=page,
            #     per_page=per_page,
            #     author_id=author_id,
            #     category_id=category_id,
            #     search=search
            # )
            
            # return {
            #     'books': [BookResponseSchema().dump(book) for book in books],
            #     'pagination': {
            #         'page': page,
            #         'per_page': per_page,
            #         'total': total,
            #         'pages': (total + per_page - 1) // per_page
            #     }
            # }
            books = book_service.get_books()
            return {
                'books': [BookResponseSchema().dump(book) for book in books]
            }
        except Exception as e:
            print(f"Error in {book_ns.name} namespace:", e)
            return {'error': 'Failed to retrieve books'}, 500


@book_ns.route('/<int:book_id>')
class Book(Resource):
    @book_ns.doc('get_book')
    def get(self, book_id):
        """Get specific book details"""
        try:
            book = book_service.get_book_by_id(book_id)
            if not book:
                return {'error': 'Book not found'}, 404
            return BookResponseSchema().dump(book)
        except Exception as e:
            return {'error': 'Failed to retrieve book'}, 500

    @book_ns.doc('update_book')
    def patch(self, book_id):
        """Update book details (admin only)"""
        try:
            data = request.get_json()
            # Validate with existing Marshmallow schema
            schema = BookUpdateSchema()
            validated_data = schema.load(data)
            
            book = book_service.update_book(book_id, validated_data)
            if not book:
                return {'error': 'Book not found'}, 404
            return BookResponseSchema().dump(book)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to update book'}, 500