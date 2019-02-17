from marshmallow.validate import Validator


class ForbidBlankStr(Validator):
    """
    Will not invalidate when field is not supplied or a None value is supplied.
    Use the 'required' parameter to invalidate no field supplied and 'allow_none' parameter to invalidate a None value.
    """

    def __init__(self, forbid_whitespace_str=False, error=None):  # whitespace str only contains whitespace characters
        pass

    def __call__(self, value):
        pass

    def _repr_args(self):
        pass
