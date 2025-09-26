from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
import secrets 

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

api = Api(
    title="Online Library API", 
    version="1.0", 
    description="Flask-RESTX API for Online Library System",
    security="Bearer Auth",
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
        }
    }
)


def create_app(config_object=None) -> Flask:
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        load_dotenv()
        # Default fallback config
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL","sqlite:///library.db"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', "127721960582844795764816642902295266977"),
            JWT_ACCESS_TOKEN_EXPIRES=False,
            JWT_REFRESH_TOKEN_EXPIRES=False
        )

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    
    # JWT Error Handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization header is required'}, 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return {'error': 'Fresh token required'}, 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has been revoked'}, 401

    from app.controllers import (
        book_controller, 
        user_controller
    )
    api.add_namespace(book_controller.book_ns, path='/api/books')
    api.add_namespace(user_controller.user_ns, path='/api/users')
    return app


