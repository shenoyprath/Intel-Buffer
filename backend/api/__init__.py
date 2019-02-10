import os

from flask import Blueprint

from flask_restplus import Api
from flask_jwt_extended import JWTManager

from redis import Redis


api_blueprint = Blueprint("api", __name__, url_prefix="/api")
rest_api = Api(api_blueprint)
jwt = JWTManager()


redis_pass_environ_var = "REDIS_DB_PASS"
if os.environ.get(redis_pass_environ_var) is None:
    raise RuntimeError(f"Environment variable {redis_pass_environ_var} isn't set to the password used to access the"
                       f"Redis database")

redis_db = Redis(host="127.0.0.1",
                 port=6379,
                 decode_responses=True,
                 password=os.environ.get(redis_pass_environ_var))

from api import auth_token
