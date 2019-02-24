class Abstract:
    """
    Tables won't be created for models that are **DIRECT** subclasses of this class.
    Using the built-in ABC module to create abstract models is not supported by peewee and will generate conflict with
    meta classes.

    Note: This class is not supposed to implement functionality provided by ABC.
    It purely exists to tell the functions in table_modifiers.py whether the model can have a table in the database.
    """
