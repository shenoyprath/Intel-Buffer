from peewee import Model

from models import db


class Base(Model):
    class Meta:
        database = db

    @classmethod
    def instantiate(cls, **query):
        """
        Abstract method for creating instances of models.
        If complex logic is needed before creating an instance, simply override this method and add the additional
        functionality before creating the instance.

        Note: This method is used because Peewee advices against overriding `Model.__init__` or `Model.create`.
        Named 'instantiate' to avoid conflict with `Model.create`.
        https://github.com/coleifer/peewee/issues/856

        :param query: Same parameters that are passed to the Peewee's 'Model.create'.
        :return: New instance of the the model.
        """

        return cls.create(**query)

    @classmethod
    def retrieve(cls, identity):
        """
        Abstract method to retrieve an instance from a model using a unique identifier.

        :param identity: Default unique identifier is the id. Named 'identity' to avoid shadowing built-in name 'id'.
        :return: Instance that matches the identifier or None if nothing matches.
        """

        return cls.get_or_none(id=identity)
