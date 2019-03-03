from marshmallow import Schema
from marshmallow.fields import Field


class Base(Schema):
    pass


Field.default_error_messages["required"] = "This field is required."
