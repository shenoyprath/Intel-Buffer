from flask import jsonify
from werkzeug.security import check_password_hash

from flask_restplus import Resource
from flask_jwt_extended import create_access_token

from api import rest_api

from models import db
from models.user import User


@rest_api.route("/auth_token/", methods=("POST",))
class AuthToken(Resource):
    @staticmethod
    def post():
        """
        Creates a new authentication token for the client if client exists in the database.

        :return JSON: Access token if client is validated or error message if client is not.
        """

        email_address = rest_api.payload.get("email_address")
        password = rest_api.payload.get("password")

        with db:
            user = User.retrieve(email_address=email_address)
            if user and check_password_hash(user.password, password):
                access_token = create_access_token(email_address)
                response = jsonify(access_token=access_token)
                response.status_code = 200
                return response

        response = jsonify(error_message="Invalid credentials. Please try again.")
        response.status_code = 401
        return response
