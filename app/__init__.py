from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api(title="Online Library API", version="1.0", description="Flask-RESTX API for Online Library System")


def create_app(config_object: str | None = None) -> Flask:
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="sqlite:///library.db",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # # Import controllers to register namespaces
    # with app.app_context():
    #     from app.controllers import book_controller  # noqa: F401
    from app.controllers import book_controller
    api.add_namespace(book_controller.book_ns, path='/api/books')

    return app


