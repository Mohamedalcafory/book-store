from flask import Blueprint, request, jsonify
from typing import Dict, Any

from app.services.book_service import BookService
from app.schemas.book_schemas import BookCreateSchema, BookUpdateSchema, BookResponseSchema
from app.utils.decorators import admin_required, validate_json


book_bp = Blueprint('books', __name__, url_prefix='/api/books')


@book_bp.route('', methods=['POST'])
# @admin_required
@validate_json(BookCreateSchema)
def create_book():
    """Create a new book (admin only)"""
    try:
        data = request.get_json()
        book = BookService.create_book(data)
        return jsonify(BookResponseSchema().dump(book)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create book'}), 500


@book_bp.route('', methods=['GET'])
def list_books():
    """List books with optional filtering and pagination"""
    try:
        # Extract query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        author_id = request.args.get('author_id', type=int)
        category_id = request.args.get('category_id', type=int)
        search = request.args.get('search', type=str)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
            
        books, total = BookService.get_books_paginated(
            page=page,
            per_page=per_page,
            author_id=author_id,
            category_id=category_id,
            search=search
        )
        
        return jsonify({
            'books': [BookResponseSchema().dump(book) for book in books],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve books'}), 500


@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    """Get specific book details"""
    try:
        book = BookService.get_book_by_id(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        return jsonify(BookResponseSchema().dump(book)), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve book'}), 500


@book_bp.route('/<int:book_id>', methods=['PATCH'])
@admin_required
@validate_json(BookUpdateSchema)
def update_book(book_id: int):
    """Update book details (admin only)"""
    try:
        data = request.get_json()
        book = BookService.update_book(book_id, data)
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        return jsonify(BookResponseSchema().dump(book)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to update book'}), 500
