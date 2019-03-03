from pytest import fixture

from app import create_app
from config import TestConfig

from api import init_redis_db


@fixture
def app():
    return create_app(TestConfig)


@fixture
def redis_database():
    yield init_redis_db(TestConfig)


@fixture
def valid_user_info():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email_address": "example@example.com",
        "password": "Password123"
    }
