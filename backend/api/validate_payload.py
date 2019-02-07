from flask import jsonify

from marshmallow import ValidationError

from api import rest_api


def validate_payload(schema):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                schema().load(rest_api.payload)
                return function(*args, **kwargs)

            except ValidationError as e:
                return jsonify(error_messages=e.messages)

        return wrapper
    return decorator
