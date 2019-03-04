from flask_restplus import Resource
from webargs.flaskparser import use_args

from api import rest_api
from api.auth_token import AuthToken

from schemas.registration_schema import RegistrationSchema


@rest_api.route("/user", methods=("POST",))
class User(Resource):
    @staticmethod
    @use_args(RegistrationSchema(), error_status_code=422)
    def post(new_user):
        tokens = AuthToken.create_tokens(new_user)
        return AuthToken.serialize(*tokens)
