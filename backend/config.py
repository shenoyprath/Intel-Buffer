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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ("refresh",)
    JWT_TOKEN_LOCATION = ("cookies",)
    JWT_SECURE_COOKIE = False  # Only allow JWT cookies to be sent over https. True in production.
    JWT_ACCESS_COOKIE_PATH = "/api"
    JWT_REFRESH_COOKIE_PATH = "/api/auth-token"
    # CSRF cookies' paths are not set to the access/refresh cookies' paths. If they are, the
    # client can't access CSRF cookies using JS & will not attach the cookies to the request.
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SESSION_COOKIE = False  # Cookies should be persistent.

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
    DB_NAME = "intel_buffer_prod_db"
    REDIS_DB = 2
    JWT_SECURE_COOKIE = True
