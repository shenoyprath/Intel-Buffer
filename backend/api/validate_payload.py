from functools import wraps

from flask import jsonify

from marshmallow import ValidationError

from api import rest_api


def validate_payload(schema, fail_status_code):
    """
    Decorator to wrap api routes. Automatically validates the payload against a schema.
    If payload validates, it allows the api route to handle the request.
    Otherwise, it returns the errors without calling the api route.

    :param schema: Schema to validate the payload sent by the client.
    :param fail_status_code: Status code sent to client if payload does not validate.
    """

    def decorator(route):
        @wraps(route)
        def wrapper(*args, **kwargs):
            try:
                payload = schema().load(rest_api.payload)
                return route(payload=payload.data, *args, **kwargs)

            except ValidationError as e:
                response = jsonify(error_messages=e.messages)
                response.status_code = fail_status_code
                return response

        return wrapper
    return decorator
