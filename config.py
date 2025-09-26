import os
from dotenv import load_dotenv

load_dotenv()
  
class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://root:admin@localhost:3306/bookstore"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', f'{os.urandom(32)}')
    JWT_ACCESS_TOKEN_EXPIRES = False  # We handle expiration in the service
    JWT_REFRESH_TOKEN_EXPIRES = False  # We handle expiration in the service

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
