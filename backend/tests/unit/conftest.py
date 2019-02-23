from pytest import fixture

from app import create_app
from config import TestConfig

from models import init_db
from models.base import Base


@fixture
def app():
    return create_app(TestConfig)


@fixture
def database():
    db = init_db("intel_buffer_test_db")
    models = Base.__subclasses__()

    # Don't use `with db:` here. It opens a new transaction
    # which interferes with transactions in the actual code.
    with db.connection_context():
        db.create_tables(models)
        yield db
        db.drop_tables(models)
