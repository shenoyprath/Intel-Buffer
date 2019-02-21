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
    @use_args(LoginSchema(), error_status_code=401)
    def post(args):
        """
        Creates a new authentication (access and refresh) token for the client.
        """

        email_address = args.get("email_address")

        access_token = create_access_token(email_address)
        refresh_token = create_refresh_token(email_address)

        response = jsonify(
            access_token=access_token,
            refresh_token=refresh_token
        )
        response.status_code = 200
        return response
