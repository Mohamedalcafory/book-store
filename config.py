import os
from environs import Env

env = Env()
env.read_env()

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", "sqlite:///library.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
