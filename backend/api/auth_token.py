from datetime import datetime

from flask import jsonify
from werkzeug.security import check_password_hash

from flask_restplus import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
                               get_jwt_claims, get_raw_jwt

from app import jwt

from api import rest_api, redis_db

from models import db
from models.user import User


@rest_api.route("/auth_token/", methods=("POST",))
class AuthToken(Resource):
    @staticmethod
    @jwt.user_claims_loader
    def add_token_claims(identity):
        """
        Custom claims for the authentication tokens (mostly to find the time the token was issued at).
        """

        return {"identity": identity,
                "creation_timestamp": str(datetime.utcnow())}

    @staticmethod
    def post():
        """
        Creates a new authentication (access and refresh) token for the client if client exists in the database.

        :return JSON: Access token if client is validated or error message if client is not.
        """

        email_address = rest_api.payload.get("email_address")
        password = rest_api.payload.get("password")

        with db:
            user = User.retrieve(email_address=email_address)
            if user and check_password_hash(user.password, password):
                access_token = create_access_token(email_address)
                refresh_token = create_refresh_token(email_address)

                response = jsonify(access_token=access_token,
                                   refresh_token=refresh_token)
                response.status_code = 200
                return response

        response = jsonify(error_message="Invalid credentials. Please try again.")
        response.status_code = 401
        return response

    @staticmethod
    @jwt_required
    def delete():
        """
        Blacklists the client's authentication token till they expire. Used to "log the user out".
        No way to avoid state management here because token needs to be invalidated immediately.
        """

        token_expiration = get_jwt_claims().get("creation_timestamp")
        expiration_delta = datetime.utcnow() - datetime.strptime(token_expiration, "%Y-%m-%d %H:%M:%S.%f")

        redis_db.set(name=f"token_blacklist:{get_jwt_identity()}",
                     value=get_raw_jwt(),
                     ex=expiration_delta.total_seconds())
