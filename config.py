import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///anime.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Gunicorn workers fallback
    GUNICORN_WORKERS = int(os.environ.get('GUNICORN_WORKERS', '3'))
    GUNICORN_TIMEOUT = int(os.environ.get('GUNICORN_TIMEOUT', '30'))

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
