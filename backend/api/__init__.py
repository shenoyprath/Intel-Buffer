from flask import Blueprint

from flask_restplus import Api
from flask_jwt_extended import JWTManager

from redis import Redis

from config import DevConfig


api_blueprint = Blueprint("api", __name__, url_prefix="/api")
rest_api = Api(api_blueprint)
jwt = JWTManager()
# Restplus implements its own error handlers while JWT's error handlers are implemented with flask's native error
# handlers. Restplus catches the error before the native Flask implementation does and therefore, the error never makes
# it to Flask JWT. This means that the error messages JWT wants to throw never make it to the client. Here, we use a
# protected JWT method to add the error handlers manually to the restplus api instance.
# https://github.com/vimalloc/flask-jwt-extended/issues/83 and https://github.com/vimalloc/flask-jwt-extended/issues/86
# noinspection PyProtectedMember
jwt._set_error_handler_callbacks(rest_api)


def init_redis_db(config):
    return Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        decode_responses=True,
        password=config.REDIS_DB_PASS
    )


redis_db = init_redis_db(DevConfig)


from api import auth_token, error_handler, user  # NOQA
