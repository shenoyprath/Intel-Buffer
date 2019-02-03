from peewee import Model

from models import db


class Base(Model):
    class Meta:
        database = db
