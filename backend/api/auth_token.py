from datetime import datetime

from flask import jsonify

from flask_restplus import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from webargs.flaskparser import use_args

from api import rest_api, jwt

from schemas.login_schema import LoginSchema


@rest_api.route("/auth_token", methods=("POST",))
class AuthToken(Resource):
    @staticmethod
    @jwt.user_claims_loader
    def add_token_claims(identity):
        """
        Custom claims for the authentication tokens (mostly to find the time the token was issued at).
        """

        return {
            "identity": identity,
            "creation_timestamp": str(datetime.utcnow())
        }

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
