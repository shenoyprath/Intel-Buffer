from marshmallow import Schema


class Base(Schema):
    class Meta:
        strict = True  # schema validation failure will raise ValidationError. marshmallow 2 doesn't do this by default.
