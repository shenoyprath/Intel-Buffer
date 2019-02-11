import os

from peewee import MySQLDatabase

from models import db_user_environ_var, db_pass_environ_var
from models.base import Base


db = MySQLDatabase("intel_buffer_test_db",
                   user=os.environ.get(db_user_environ_var),
                   password=os.environ.get(db_pass_environ_var))
models = Base.__subclasses__()


class TestDatabaseAccessor:
    @classmethod
    def setup_class(cls):
        db.bind(models, bind_refs=False, bind_backrefs=False)

        db.connect()
        db.create_tables(models)

    @staticmethod
    def test_models_exist():
        for model in models:
            assert model.table_exists()

    @classmethod
    def teardown_class(cls):
        db.drop_tables(models)
        db.close()
