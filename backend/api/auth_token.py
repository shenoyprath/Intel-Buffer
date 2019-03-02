from time import time

from flask import jsonify

from flask_restplus import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_raw_jwt, jwt_required, get_jti
from webargs.flaskparser import use_args

from api import rest_api, jwt, redis_db

from schemas.login_schema import LoginSchema


@rest_api.route("/auth_token", methods=("POST", "DELETE"))
class AuthToken(Resource):

    redis_namespace = "auth_blacklist"

    @staticmethod
    def create_tokens(user):
        """
        This is mainly because JWT Extended can allow access to only of the tokens in an endpoint. However,
        when the user accesses the `DELETE` route, both tokens need to be immediately invalidated. Therefore,
        a reference to the refresh token JTI is added in the access token user claims. See issue #5 for more details.
        """

        identity = user.email_address
        refresh_token = create_refresh_token(identity)
        access_token = create_access_token(
            identity=identity,
            user_claims={
                "refresh_jti": get_jti(refresh_token)
            }
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @classmethod
    @use_args(LoginSchema(), error_status_code=401)
    def post(cls, user):
        tokens = cls.create_tokens(user)
        return jsonify(tokens)

    @classmethod
    def get_db_key(cls, token):
        return f"{cls.redis_namespace}:{token['jti']}"

    # making this a class method messes with jwt as it passes one arg without passing the class.
    @staticmethod
    @jwt.token_in_blacklist_loader
    def is_token_revoked(token):
        key = AuthToken.get_db_key(token)
        return redis_db.get(key) is not None

    @classmethod
    @jwt_required
    def delete(cls):
        """
        No way to avoid state management here because when the user logs out, the token is not immediately invalidated.
        However, some way to reject these tokens is still necessary. Therefore, the token is added to the redis database
        until it expires. Any token that's in the database is automatically rejected.
        """

        token = get_raw_jwt()
        storage_duration = token["exp"] - int(time())
        redis_db.set(
            name=cls.get_db_key(token),
            value=token["identity"],  # redis doesn't allow expiration for sets/lists.
            ex=storage_duration
        )

        return jsonify(msg="Token successfully invalidated.")
