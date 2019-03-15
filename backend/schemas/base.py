from marshmallow import Schema
from marshmallow.fields import Field


class Base(Schema):
    custom_errors = {}


# Some of the default msgs use programmer language like "Field cannot be null".
Field.default_error_messages.update(
    dict.fromkeys(["required", "null"], "This field is required.")
)
