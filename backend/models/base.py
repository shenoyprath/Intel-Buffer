from peewee import Model, DoesNotExist
from playhouse.shortcuts import model_to_dict

from models import db


class Base(Model):
    # In Peewee, an abstract meta class variable is not implemented like it is in Django's ORM.
    # To know whether a model requires a table in the database, we have to implement it ourselves.
    # Using built-in `ABC` won't work as it creates conflicts between `ABCMeta` and the Meta classes of `peewee.Model`.
    # In order for a model to be considered abstract, this variable needs to be explicitly set to True.
    # Therefore, this variable should not be moved to the Meta class as all variables in Meta end up in __dict__,
    # whether or not they're inherited or explicitly set.
    # Look at the class method `is_abstract()` for more details on implementation.
    __is_abstract = True

    class Meta:
        database = db

    @classmethod
    def instantiate(cls, *instance_args, **instance_kwargs):
        """
        Interface method for creating instances of models.
        If complex logic is needed before creating an instance, simply override this method and add the additional
        functionality before creating the instance.

        Note: This method is used instead of overriding `Base.__init__` or `Base.create` because Peewee advices against
        overriding them.
        https://github.com/coleifer/peewee/issues/856

        :return: New instance of the the model.
        """

        raise NotImplementedError

    @classmethod
    def retrieve(cls, *uid_args, **uid_kwargs):
        """
        Interface method to retrieve an instance from a model using unique identifiers other than id.

        :return: Instance of model that has the specified unique identifier values. None if no match is found.
        """

        raise NotImplementedError

    @classmethod
    def get_or_none_by_id(cls, id_):
        try:
            return cls.get_by_id(id_)
        except DoesNotExist:
            return

    @classmethod
    def is_abstract(cls):
        """
        In order for a model to be considered abstract, it needs to have `__is_abstract` explicitly defined to be True.
        This means that if a model inherits from a parent model that has set `__is_abstract` to True, the child will
        still be considered a concrete model because it doesn't explicitly define the class variable as True.
        """

        return (
            cls.__is_abstract and
            f"_{cls.__name__}__is_abstract" in cls.__dict__
        )

    @classmethod
    def get_concrete_descendants(cls):
        for descendant in cls.__subclasses__():
            if not descendant.is_abstract():
                yield descendant

            yield from descendant.get_concrete_descendants()

    def __repr__(self):
        return f"<{self.__class__.__name__} {model_to_dict(self)}>"
