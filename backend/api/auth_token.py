from flask import jsonify

from flask_restplus import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from webargs.flaskparser import use_args

from api import rest_api, jwt, redis_db

from schemas.login_schema import LoginSchema


@rest_api.route("/auth_token", methods=("POST",))
class AuthToken(Resource):

    redis_namespace = "auth_blacklist"

    @staticmethod
    def create_tokens(identity):
        return {
            "access_token": create_access_token(identity),
            "refresh_token": create_refresh_token(identity)
        }

    @classmethod
    @use_args(LoginSchema(), error_status_code=401)
    def post(cls, user):
        """
        Creates a new authentication (access and refresh) token for the client.
        """

        tokens = cls.create_tokens(user.email_address)
        return jsonify(tokens)

    @classmethod
    def concat_namespace(cls, key):
        return f"{cls.redis_namespace}:{key}"

    @classmethod
    @jwt.token_in_blacklist_loader
    def is_token_blacklisted(cls, token):
        email_address = token.get("jti")
        return redis_db.get(
            cls.concat_namespace(email_address)
        ) is not None
