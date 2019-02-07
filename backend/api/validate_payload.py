from flask import jsonify

from marshmallow import ValidationError

from api import rest_api


def validate_payload(schema, fail_status_code):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                payload = schema().load(rest_api.payload)
                return function(payload=payload.data, *args, **kwargs)

            except ValidationError as e:
                response = jsonify(error_messages=e.messages)
                response.status_code = fail_status_code
                return response

        return wrapper
    return decorator
