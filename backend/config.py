import os
from datetime import timedelta


class Config:
    ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "DevelopmentKey")

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, "frontend/dist")

    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    if not os.path.exists(DIST_DIR):  # pragma: no cover
        raise NotADirectoryError(f"DIST_DIR not found: {DIST_DIR}")


class DevConfig(Config):
    DEBUG = True
    DATABASE_NAME = "intel_buffer_db"


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_NAME = "intel_buffer_test_db"


class ProdConfig(Config):
    DEBUG = False
