import os

from peewee import MySQLDatabase
from pytest import fixture

from app import create_app

from models import db_user_environ_var, db_pass_environ_var
from models.base import Base


@fixture
def app():
    return create_app()


@fixture
def database():
    db = MySQLDatabase(
        "intel_buffer_test_db",
        user=os.getenv(db_user_environ_var),
        password=os.getenv(db_pass_environ_var),
        charset="utf8mb4"
    )
    models = Base.__subclasses__()
    db.bind(models, bind_refs=False, bind_backrefs=False)

    with db:
        db.create_tables(models)
        yield db
        db.drop_tables(models)
