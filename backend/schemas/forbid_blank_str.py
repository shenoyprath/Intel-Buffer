from marshmallow.validate import Validator, ValidationError
from marshmallow.fields import Field

from utils.is_empty_or_space import is_empty_or_space


class ForbidBlankStr(Validator):
    """
    Will not invalidate when field is not supplied or a None value is supplied.
    Use the 'required' parameter to invalidate no field supplied and 'allow_none' parameter to invalidate a None value.
    """

    def __init__(self, forbid_whitespace_str=False, error=None):  # whitespace str only contains whitespace characters
        self.forbid_whitespace_str = forbid_whitespace_str
        self.error = error or Field.default_error_messages["required"]

    def __call__(self, value):
        if value is None:  # if value=None and allow_none=False, required err msg shouldn't duplicate in err msgs dict
            return

        if (
            not value or
            (self.forbid_whitespace_str and is_empty_or_space(value))
        ):
            raise ValidationError(self.error)

    def _repr_args(self):
        return f"forbid_whitespace_str={self.forbid_whitespace_str}"
