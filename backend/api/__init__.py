import os

from flask import Blueprint

from flask_restplus import Api
from flask_jwt_extended import JWTManager

from redis import Redis

from utils.getenv_or_err import getenv_or_err


api_blueprint = Blueprint("api", __name__, url_prefix="/api")
rest_api = Api(api_blueprint)
jwt = JWTManager()


redis_pass_environ_var = "REDIS_DB_PASS"
getenv_or_err(redis_pass_environ_var)

redis_db = Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
    password=os.getenv(redis_pass_environ_var)
)


from api import auth_token, error_handler, user
