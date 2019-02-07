from marshmallow import Schema


class Base(Schema):
    class Meta:
        strict = True  # failure to validate the schema raises a ValidationError
