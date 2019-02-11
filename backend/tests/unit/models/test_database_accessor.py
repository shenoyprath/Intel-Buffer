import os
from functools import wraps

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


def database_accessor(test_case):
    """
    Decorator for wrapping a test case to get method level database setup and teardown.
    """

    @wraps(test_case)
    def wrapper(*args, **kwargs):
        database_setup()
        result = test_case(*args, **kwargs)
        database_teardown()

        return result

    return wrapper


@database_accessor
def test_models_exist():
    assert all(model.table_exists() for model in models)


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
