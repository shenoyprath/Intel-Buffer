from flask import jsonify

from flask_restplus import Resource
from webargs.flaskparser import use_args

from api import rest_api
from api.auth_token import AuthToken

from models.user import User as UserModel

from schemas.registration_schema import RegistrationSchema


@rest_api.route("/user", methods=("POST",))
class User(Resource):
    @staticmethod
    @use_args(RegistrationSchema(), error_status_code=422)
    def post(user_details):
        new_user = UserModel.instantiate(**user_details)
        tokens = AuthToken.create_tokens(new_user.email_address)

        return jsonify(tokens)
