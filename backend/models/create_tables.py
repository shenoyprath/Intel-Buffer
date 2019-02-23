from models.base import Base, AbstractModel


def create_tables(base_cls=Base):
    """
    It can be annoying to keep importing new models and creating a table for each of them.
    This function automates the process by recursively creating tables for the  base class and all of its subclasses.
    Tables will only be created for a class/subclass if that that particular class/subclass doesn't inherit **DIRECTLY**
    from AbstractModel.

    :param base_cls: Base class used as the starting point of recursion for recursively creating the tables.
    """

    if AbstractModel not in base_cls.__bases__:
        base_cls.create_table()

    for model in base_cls.__subclasses__():
        create_tables(base_cls=model)
