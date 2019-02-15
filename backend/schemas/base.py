from marshmallow import Schema
from marshmallow.fields import Field


Field.default_error_messages["required"] = "This field is required."


class Base(Schema):
    class Meta:
        strict = True  # schema validation failure will raise ValidationError. marshmallow 2 doesn't do this by default.
