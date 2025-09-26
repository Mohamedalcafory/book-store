from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from typing import Optional


class UserRegistrationSchema(Schema):
    """Schema for user registration"""
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username can only contain letters, numbers, and underscores')
        ]
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, max=128),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
                error='Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character'
            )
        ]
    )
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('Passwords do not match', 'confirm_password')


class UserLoginSchema(Schema):
    """Schema for user login"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserResponseSchema(Schema):
    """Schema for user response (without sensitive data)"""
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    is_active = fields.Bool()
    is_admin = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class UserUpdateSchema(Schema):
    """Schema for updating user profile"""
    username = fields.Str(
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username can only contain letters, numbers, and underscores')
        ]
    )
    email = fields.Email()
    current_password = fields.Str(required=True)
    new_password = fields.Str(
        validate=[
            validate.Length(min=8, max=128),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
                error='Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character'
            )
        ]
    )


class TokenResponseSchema(Schema):
    """Schema for authentication token response"""
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserResponseSchema)