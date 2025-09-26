from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from typing import Dict, Any

from app.services.category_service import category_service
from app.schemas.category_schemas import CategoryCreateSchema, CategoryUpdateSchema, CategoryResponseSchema

# Create namespace for Swagger documentation
category_ns = Namespace('categories', description='Category operations', security='Bearer Auth')


category_create_model = category_ns.model(
    "CategoryCreate",
    {
        "name": fields.String(required=True, description="Category name"),
        "description": fields.String(description="Category description"),
    },
)

category_update_model = category_ns.model(
    "CategoryUpdate",
    {
        "name": fields.String(description="Category name"),
        "description": fields.String(description="Category description"),
    },
)

category_model = category_ns.model(
    "Category",
    {
        "id": fields.Integer(readOnly=True, description="Category ID"),
        "name": fields.String(required=True, description="Category name"),
        "description": fields.String(description="Category description"),
        "created_at": fields.DateTime(readOnly=True, description="Creation timestamp"),
        "updated_at": fields.DateTime(readOnly=True, description="Last update timestamp"),
        "books_count": fields.Integer(readOnly=True, description="Number of books in this category"),
    },
)

pagination_model = category_ns.model(
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

category_list_model = category_ns.model(
    "CategoryList",
    {
        "categories": fields.Nested(category_model, many=True),
        "pagination": fields.Nested(pagination_model),
    },
)


@category_ns.route('')
class CategoryList(Resource):
    @category_ns.doc('create_category', security='Bearer Auth')
    @category_ns.expect(category_create_model)
    @category_ns.marshal_with(category_model, code=201)
    @category_ns.response(400, 'Validation Error')
    @category_ns.response(401, 'Authentication required')
    @category_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def post(self):
        """Create a new category"""
        try:
            data = request.get_json()
            # Validate with existing Marshmallow schema
            schema = CategoryCreateSchema()
            validated_data = schema.load(data)
            
            category = category_service.create_category(validated_data)
            return CategoryResponseSchema().dump(category), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            print(f"Error in {category_ns.name} namespace:", e)
            return {'error': 'Failed to create category'}, 500

    @category_ns.doc('list_categories', security='Bearer Auth')
    @category_ns.marshal_with(category_list_model)
    @category_ns.response(401, 'Authentication required')
    @category_ns.response(500, 'Internal Server Error')
    @category_ns.param('page', 'Page number', type=int, default=1)
    @category_ns.param('per_page', 'Items per page (max 100)', type=int, default=10)
    @category_ns.param('search', 'Search categories by name', type=str)
    @jwt_required()
    def get(self):
        """List categories with optional filtering and pagination"""
        try:
            # Extract query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', type=str)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:
                per_page = 10
                
            categories, total = category_service.get_categories_paginated(
                page=page,
                per_page=per_page,
                search=search
            )
            schema = CategoryResponseSchema(many=True)
            return {
                'categories': schema.dump(categories.items),
                'pagination': {
                    'page': categories.page,
                    'per_page': categories.per_page,
                    'total': total,
                    'pages': categories.pages,
                    'has_next': categories.has_next,
                    'has_prev': categories.has_prev,
                    'next_num': categories.next_num,
                    'prev_num': categories.prev_num,
                }
            }
        except Exception as e:
            print(f"Error in {category_ns.name} namespace:", e)
            return {'error': 'Failed to retrieve categories'}, 500


@category_ns.route('/<int:category_id>')
@category_ns.param('category_id', 'The category identifier', type=int)
class Category(Resource):
    @category_ns.doc('get_category', security='Bearer Auth')
    @category_ns.marshal_with(category_model)
    @category_ns.response(401, 'Authentication required')
    @category_ns.response(404, 'Category not found')
    @category_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def get(self, category_id):
        """Get specific category details"""
        try:
            category = category_service.get_category_by_id(category_id)
            if not category:
                return {'error': 'Category not found'}, 404
            return CategoryResponseSchema().dump(category)
        except Exception as e:
            return {'error': 'Failed to retrieve category'}, 500

    @category_ns.doc('update_category', security='Bearer Auth')
    @category_ns.expect(category_update_model)
    @category_ns.marshal_with(category_model)
    @category_ns.response(400, 'Validation Error')
    @category_ns.response(401, 'Authentication required')
    @category_ns.response(404, 'Category not found')
    @category_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def patch(self, category_id):
        """Update category details"""
        try:
            data = request.get_json()
            # Validate with existing Marshmallow schema
            schema = CategoryUpdateSchema()
            validated_data = schema.load(data)
            
            category = category_service.update_category(category_id, validated_data)
            if not category:
                return {'error': 'Category not found'}, 404
            schema = CategoryResponseSchema()
            return schema.dump(category)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to update category'}, 500

    @category_ns.doc('delete_category', security='Bearer Auth')
    @category_ns.response(204, 'Category deleted successfully')
    @category_ns.response(400, 'Cannot delete category with books')
    @category_ns.response(401, 'Authentication required')
    @category_ns.response(404, 'Category not found')
    @category_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def delete(self, category_id):
        """Delete a category"""
        try:
            success = category_service.delete_category(category_id)
            if not success:
                return {'error': 'Category not found'}, 404
            return '', 204
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to delete category'}, 500
