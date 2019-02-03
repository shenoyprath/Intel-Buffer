from peewee import Model

from models import db


class Base(Model):
    class Meta:
        database = db

    @classmethod
    def instantiate(cls, **query):
        """
        Factory method for creating instances of models.
        If complex logic is needed before creating an instance, simply override this method and add the additional
        functionality before creating the instance.

        Note: This method is used because Peewee advices against overriding `Model.__init__` or `Model.create`.
        Named 'instantiate' to avoid conflict with `Model.create`.
        https://github.com/coleifer/peewee/issues/856
        """

        return cls.create(**query)
