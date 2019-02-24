from _pytest.fixtures import fixture

from app import create_app
from config import TestConfig


@fixture
def app():
    return create_app(TestConfig)
