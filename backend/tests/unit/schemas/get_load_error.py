from pytest import raises

from marshmallow import ValidationError


def get_load_error(schema, payload):
    with raises(ValidationError) as e:
        schema().load(payload)
    return e
