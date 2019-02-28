from time import time

from flask import jsonify

from flask_restplus import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt, jwt_required
from webargs.flaskparser import use_args

from api import rest_api, jwt, redis_db

from schemas.login_schema import LoginSchema


@rest_api.route("/auth_token", methods=("POST", "DELETE"))
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

    # making this a class method messes with jwt as it passes one arg without passing the class.
    @staticmethod
    @jwt.token_in_blacklist_loader
    def is_token_blacklisted(token):
        email_address = token.get("identity")
        return redis_db.get(
            AuthToken.concat_namespace(email_address)
        ) is not None

    @classmethod
    @jwt_required
    def delete(cls):
        """
        When the user logs out, the token is not immediately invalidated.
        However, some way to reject these tokens is still necessary.
        Therefore, the token is added to a redis database until it expires and any token that's in the database is
        automatically rejected. No way to avoid state management here.
        """

        email_address = get_jwt_identity()
        jwt_id = get_raw_jwt().get("jti")

        expiration_time = get_raw_jwt().get("exp")
        storage_delta = expiration_time - int(time())
        redis_db.set(
            name=cls.concat_namespace(email_address),
            value=jwt_id,
            ex=storage_delta
        )

        response = jsonify(msg="Token successfully invalidated.")
        return response
