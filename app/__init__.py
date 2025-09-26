from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

api = Api(title="Online Library API", version="1.0", description="Flask-RESTX API for Online Library System")


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
        )

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    
    # Initialize JWT
    jwt.init_app(app)
    
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # We handle expiration in the service
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False  # We handle expiration in the service

    from app.controllers import book_controller, user_controller
    api.add_namespace(book_controller.book_ns, path='/api/books')
    api.add_namespace(user_controller.user_ns, path='/api/users')

    return app


