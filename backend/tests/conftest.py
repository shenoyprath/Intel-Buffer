from pytest import fixture

from config import TestConfig

from models import init_db
from models.table_modifiers import create_tables, drop_tables


@fixture
def database():
    db = init_db(TestConfig)

    # Don't use `with db:` here. It opens a new transaction
    # which interferes with transactions in the actual code.
    with db.connection_context():
        create_tables()
        yield db
        drop_tables()
