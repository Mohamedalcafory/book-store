from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from typing import Dict, Any

from app.services.author_service import author_service
from app.schemas.author_schemas import AuthorCreateSchema, AuthorUpdateSchema, AuthorResponseSchema

# Create namespace for Swagger documentation
author_ns = Namespace('authors', description='Author operations')


author_create_model = author_ns.model(
    "AuthorCreate",
    {
        "name": fields.String(required=True, description="Author's full name"),
        "biography": fields.String(description="Author's biography"),
        "date_of_birth": fields.String(description="Date of birth (YYYY-MM-DD)"),
        "country": fields.String(description="Author's country"),
    },
)

author_update_model = author_ns.model(
    "AuthorUpdate",
    {
        "name": fields.String(description="Author's full name"),
        "biography": fields.String(description="Author's biography"),
        "date_of_birth": fields.String(description="Date of birth (YYYY-MM-DD)"),
        "country": fields.String(description="Author's country"),
    },
)

author_model = author_ns.model(
    "Author",
    {
        "id": fields.Integer(readOnly=True, description="Author ID"),
        "name": fields.String(required=True, description="Author's full name"),
        "biography": fields.String(description="Author's biography"),
        "date_of_birth": fields.String(description="Date of birth (YYYY-MM-DD)"),
        "country": fields.String(description="Author's country"),
        "created_at": fields.DateTime(readOnly=True, description="Creation timestamp"),
        "updated_at": fields.DateTime(readOnly=True, description="Last update timestamp"),
        "books_count": fields.Integer(readOnly=True, description="Number of books by this author"),
    },
)

pagination_model = author_ns.model(
    "Pagination",
    {
        "page": fields.Integer(description="Current page number"),
        "per_page": fields.Integer(description="Items per page"),
        "total": fields.Integer(description="Total number of items"),
        "pages": fields.Integer(description="Total number of pages"),
        "has_next": fields.Boolean(description="Whether there is a next page"),
        "has_prev": fields.Boolean(description="Whether there is a previous page"),
        "next_num": fields.Integer(description="Next page number"),
        "prev_num": fields.Integer(description="Previous page number"),
    },
)

author_list_model = author_ns.model(
    "AuthorList",
    {
        "authors": fields.Nested(author_model, many=True),
        "pagination": fields.Nested(pagination_model),
    },
)


@author_ns.route('')
class AuthorList(Resource):
    @author_ns.doc('create_author')
    @author_ns.expect(author_create_model)
    @author_ns.marshal_with(author_model, code=201)
    @author_ns.response(400, 'Validation Error')
    @author_ns.response(401, 'Authentication required')
    @author_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def post(self):
        """Create a new author"""
        try:
            data = request.get_json()
            # Validate with existing Marshmallow schema
            schema = AuthorCreateSchema()
            validated_data = schema.load(data)
            
            author = author_service.create_author(validated_data)
            return AuthorResponseSchema().dump(author), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            print(f"Error in {author_ns.name} namespace:", e)
            return {'error': 'Failed to create author'}, 500

    @author_ns.doc('list_authors')
    @author_ns.marshal_with(author_list_model)
    @author_ns.response(401, 'Authentication required')
    @author_ns.response(500, 'Internal Server Error')
    @author_ns.param('page', 'Page number', type=int, default=1)
    @author_ns.param('per_page', 'Items per page (max 100)', type=int, default=10)
    @author_ns.param('search', 'Search authors by name', type=str)
    @author_ns.param('country', 'Filter by country', type=str)
    @jwt_required()
    def get(self):
        """List authors with optional filtering and pagination"""
        try:
            # Extract query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', type=str)
            country = request.args.get('country', type=str)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:
                per_page = 10
                
            authors, total = author_service.get_authors_paginated(
                page=page,
                per_page=per_page,
                search=search,
                country=country
            )
            schema = AuthorResponseSchema(many=True)
            return {
                'authors': schema.dump(authors.items),
                'pagination': {
                    'page': authors.page,
                    'per_page': authors.per_page,
                    'total': total,
                    'pages': authors.pages,
                    'has_next': authors.has_next,
                    'has_prev': authors.has_prev,
                    'next_num': authors.next_num,
                    'prev_num': authors.prev_num,
                }
            }
        except Exception as e:
            print(f"Error in {author_ns.name} namespace:", e)
            return {'error': 'Failed to retrieve authors'}, 500


@author_ns.route('/<int:author_id>')
@author_ns.param('author_id', 'The author identifier', type=int)
class Author(Resource):
    @author_ns.doc('get_author')
    @author_ns.marshal_with(author_model)
    @author_ns.response(401, 'Authentication required')
    @author_ns.response(404, 'Author not found')
    @author_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def get(self, author_id):
        """Get specific author details"""
        try:
            author = author_service.get_author_by_id(author_id)
            if not author:
                return {'error': 'Author not found'}, 404
            return AuthorResponseSchema().dump(author)
        except Exception as e:
            return {'error': 'Failed to retrieve author'}, 500

    @author_ns.doc('update_author')
    @author_ns.expect(author_update_model)
    @author_ns.marshal_with(author_model)
    @author_ns.response(400, 'Validation Error')
    @author_ns.response(401, 'Authentication required')
    @author_ns.response(404, 'Author not found')
    @author_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def patch(self, author_id):
        """Update author details"""
        try:
            data = request.get_json()
            # Validate with existing Marshmallow schema
            schema = AuthorUpdateSchema()
            validated_data = schema.load(data)
            
            author = author_service.update_author(author_id, validated_data)
            if not author:
                return {'error': 'Author not found'}, 404
            schema = AuthorResponseSchema()
            return schema.dump(author)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to update author'}, 500

    @author_ns.doc('delete_author')
    @author_ns.response(204, 'Author deleted successfully')
    @author_ns.response(400, 'Cannot delete author with books')
    @author_ns.response(401, 'Authentication required')
    @author_ns.response(404, 'Author not found')
    @author_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def delete(self, author_id):
        """Delete an author"""
        try:
            success = author_service.delete_author(author_id)
            if not success:
                return {'error': 'Author not found'}, 404
            return '', 204
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to delete author'}, 500
