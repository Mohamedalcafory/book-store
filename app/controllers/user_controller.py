from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from marshmallow import ValidationError as MarshmallowValidationError
from app.services.user_service import UserService
from app.schemas.user_schemas import (
    UserRegistrationSchema, 
    UserLoginSchema, 
    UserResponseSchema, 
    UserUpdateSchema,
    TokenResponseSchema
)
from app.utils.exceptions import ValidationError, AuthenticationError, UserNotFoundError

# Create namespace for Swagger documentation
user_ns = Namespace('users', description='User authentication and management operations')

# Initialize service
user_service = UserService()

# Initialize schemas
registration_schema = UserRegistrationSchema()
login_schema = UserLoginSchema()
user_response_schema = UserResponseSchema()
user_update_schema = UserUpdateSchema()
token_response_schema = TokenResponseSchema()

# Define API models for Swagger documentation
user_registration_model = user_ns.model(
    "UserRegistration",
    {
        "username": fields.String(required=True, description="Username (3-50 characters, alphanumeric and underscores only)"),
        "email": fields.String(required=True, description="Valid email address"),
        "password": fields.String(required=True, description="Password (min 8 chars, must contain uppercase, lowercase, digit, and special character)"),
        "confirm_password": fields.String(required=True, description="Password confirmation")
    }
)

user_login_model = user_ns.model(
    "UserLogin",
    {
        "username": fields.String(required=True, description="Username or email"),
        "password": fields.String(required=True, description="Password")
    }
)

user_response_model = user_ns.model(
    "UserResponse",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "is_active": fields.Boolean(),
        "is_admin": fields.Boolean(),
        "created_at": fields.DateTime(),
        "updated_at": fields.DateTime()
    }
)

user_update_model = user_ns.model(
    "UserUpdate",
    {
        "username": fields.String(description="New username"),
        "email": fields.String(description="New email"),
        "current_password": fields.String(required=True, description="Current password for verification")
    }
)

password_change_model = user_ns.model(
    "PasswordChange",
    {
        "current_password": fields.String(required=True, description="Current password"),
        "new_password": fields.String(required=True, description="New password (min 8 chars, must contain uppercase, lowercase, digit, and special character)")
    }
)

token_response_model = user_ns.model(
    "TokenResponse",
    {
        "access_token": fields.String(),
        "refresh_token": fields.String(),
        "user": fields.Nested(user_response_model)
    }
)


@user_ns.route('/signUp')
class UserRegistration(Resource):
    @user_ns.doc('register_user')
    @user_ns.expect(user_registration_model)
    @user_ns.marshal_with(token_response_model, code=201)
    @user_ns.response(400, 'Validation Error')
    @user_ns.response(500, 'Internal Server Error')
    def post(self):
        """Register a new user"""
        try:
            # Validate input data
            data = registration_schema.load(request.json)
            
            # Register user
            user, tokens = user_service.register_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            
            # Prepare response
            response_data = {
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'user': user_response_schema.dump(user)
            }
            
            return response_data, 201
            
        except MarshmallowValidationError as e:
            user_ns.abort(400, 'Validation error', errors=e.messages)
        except ValidationError as e:
            user_ns.abort(400, str(e))
        except Exception as e:
            user_ns.abort(500, 'Internal server error')


@user_ns.route('/login')
class UserLogin(Resource):
    @user_ns.doc('login_user')
    @user_ns.expect(user_login_model)
    @user_ns.marshal_with(token_response_model)
    @user_ns.response(400, 'Validation Error')
    @user_ns.response(500, 'Internal Server Error')
    def post(self):
        """Login user"""
        try:
            # Validate input data
            data = login_schema.load(request.json)
            
            # Authenticate user
            user, tokens = user_service.login_user(
                username=data['username'],
                password=data['password']
            )
            
            # Prepare response
            response_data = {
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'user': user_response_schema.dump(user)
            }
            
            return response_data, 200
            
        except MarshmallowValidationError as e:
            user_ns.abort(400, 'Validation error', errors=e.messages)
        except AuthenticationError as e:
            user_ns.abort(401, str(e))
        except Exception as e:
            user_ns.abort(500, 'Internal server error')


@user_ns.route('/profile')
class UserProfile(Resource):
    @user_ns.doc('get_user_profile')
    @user_ns.marshal_with(user_response_model)
    @user_ns.response(404, 'User not found')
    @user_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def get(self):
        """Get current user profile"""
        try:
            current_user_id = get_jwt_identity()
            user = user_service.get_user_by_id(current_user_id)
            
            if not user:
                user_ns.abort(404, 'User not found')
            
            return user_response_schema.dump(user), 200
            
        except Exception as e:
            user_ns.abort(500, 'Internal server error')

    @user_ns.doc('update_user_profile')
    @user_ns.expect(user_update_model)
    @user_ns.marshal_with(user_response_model)
    @user_ns.response(400, 'Validation Error')
    @user_ns.response(404, 'User not found')
    @user_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def put(self):
        """Update current user profile"""
        try:
            current_user_id = get_jwt_identity()
            
            # Validate input data
            data = user_update_schema.load(request.json)
            
            # Update user profile
            user = user_service.update_user_profile(
                user_id=current_user_id,
                username=data.get('username'),
                email=data.get('email')
            )
            
            return user_response_schema.dump(user), 200
            
        except MarshmallowValidationError as e:
            user_ns.abort(400, 'Validation error', errors=e.messages)
        except ValidationError as e:
            user_ns.abort(400, str(e))
        except UserNotFoundError as e:
            user_ns.abort(404, str(e))
        except Exception as e:
            user_ns.abort(500, 'Internal server error')


@user_ns.route('/change-password')
class PasswordChange(Resource):
    @user_ns.doc('change_password')
    @user_ns.expect(password_change_model)
    @user_ns.response(200, 'Password changed successfully')
    @user_ns.response(400, 'Validation Error')
    @user_ns.response(401, 'Authentication Error')
    @user_ns.response(404, 'User not found')
    @user_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def post(self):
        """Change user password"""
        try:
            current_user_id = get_jwt_identity()
            
            data = request.json
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            
            if not current_password or not new_password:
                user_ns.abort(400, 'Current password and new password are required')
            
            # Change password
            user_service.change_password(
                user_id=current_user_id,
                current_password=current_password,
                new_password=new_password
            )
            
            return {'message': 'Password changed successfully'}, 200
            
        except AuthenticationError as e:
            user_ns.abort(401, str(e))
        except ValidationError as e:
            user_ns.abort(400, str(e))
        except UserNotFoundError as e:
            user_ns.abort(404, str(e))
        except Exception as e:
            user_ns.abort(500, 'Internal server error')


@user_ns.route('/refresh')
class TokenRefresh(Resource):
    @user_ns.doc('refresh_token')
    @user_ns.response(200, 'Token refreshed successfully')
    @user_ns.response(404, 'User not found or inactive')
    @user_ns.response(500, 'Internal Server Error')
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        try:
            current_user_id = get_jwt_identity()
            user = user_service.get_user_by_id(current_user_id)
            
            if not user or not user.is_active:
                user_ns.abort(404, 'User not found or inactive')
            
            # Create new access token
            access_token = create_access_token(
                identity=current_user_id,
                additional_claims={
                    'username': user.username,
                    'is_admin': user.is_admin
                }
            )
            
            return {'access_token': access_token}, 200
            
        except Exception as e:
            user_ns.abort(500, 'Internal server error')


@user_ns.route('/logout')
class UserLogout(Resource):
    @user_ns.doc('logout_user')
    @user_ns.response(200, 'Logged out successfully')
    @user_ns.response(500, 'Internal Server Error')
    @jwt_required()
    def post(self):
        """Logout user (client should discard tokens)"""
        return {'message': 'Logged out successfully'}, 200
