from peewee import Model, DoesNotExist
from playhouse.shortcuts import model_to_dict

from models import db
from models.abstract import Abstract


class Base(Abstract, Model):
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

        :return: Instance of model that has the specified unique identifier values.
        """

        raise NotImplementedError

    @classmethod
    def safe_get_by_id(cls, id_):
        """
        Abstract method that essentially implements a get_or_none_by_id method.
        """

        try:
            return cls.get_by_id(id_)
        except DoesNotExist:
            return

    @classmethod
    def is_concrete(cls):
        """
        Concrete models are models that are not **DIRECT** subclasses of the Abstract model.
        """

        return Abstract not in cls.__bases__

    @classmethod
    def get_concrete_descendants(cls):
        for descendant in cls.__subclasses__():
            if descendant.is_concrete():
                yield descendant

            yield from descendant.get_concrete_descendants()

    def __repr__(self):
        return f"<{self.__class__.__name__} {model_to_dict(self)}>"
