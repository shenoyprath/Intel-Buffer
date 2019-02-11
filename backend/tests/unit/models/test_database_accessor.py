import os

from peewee import MySQLDatabase

from models import db_user_environ_var, db_pass_environ_var
from models.base import Base


db = MySQLDatabase("intel_buffer_test_db",
                   user=os.environ.get(db_user_environ_var),
                   password=os.environ.get(db_pass_environ_var))
models = Base.__subclasses__()


def database_setup():
    db.bind(models, bind_refs=False, bind_backrefs=False)

    db.connect()
    db.create_tables(models)


def database_teardown():
    db.drop_tables(models)
    db.close()


def test_models_exist():
    database_setup()

    for model in models:
        assert model.table_exists()

    database_teardown()


class DatabaseAccessor:
    """
    Inherit this class in order to receive class level database setup and teardown.
    """

    @classmethod
    def setup_class(cls):
        database_setup()

    @classmethod
    def teardown_class(cls):
        database_teardown()
