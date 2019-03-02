import os
from abc import ABC
from datetime import timedelta

from utils.getenv_or_err import getenv_or_err


class Config(ABC):
    SECRET_KEY = getenv_or_err("FLASK_SECRET_KEY")

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, "frontend/dist")

    DB_USER = getenv_or_err("INTEL_BUFFER_DB_USER")
    DB_PASS = getenv_or_err("INTEL_BUFFER_DB_PASS")

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB_PASS = getenv_or_err("REDIS_DB_PASS")

    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ("access", "refresh")

    if not os.path.exists(DIST_DIR):  # pragma: no cover
        raise NotADirectoryError(f"DIST_DIR not found: {DIST_DIR}")


class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    DB_NAME = "intel_buffer_db"
    REDIS_DB = 0


class TestConfig(Config):
    ENV = "testing"
    DEBUG = True
    TESTING = True
    DB_NAME = "intel_buffer_test_db"
    REDIS_DB = 1


class ProdConfig(Config):
    ENV = "production"
    DEBUG = False
    REDIS_DB = 2
