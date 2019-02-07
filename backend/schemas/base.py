from marshmallow import Schema


class Base(Schema):
    class Meta:
        strict = True  # raises ValidationError when fails to validate the schema
