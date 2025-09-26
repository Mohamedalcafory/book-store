from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

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

    from app.controllers import book_controller
    api.add_namespace(book_controller.book_ns, path='/api/books')

    return app


