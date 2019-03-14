from time import time

from flask_restplus import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_raw_jwt, get_jwt_identity, jwt_refresh_token_required,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from webargs.flaskparser import use_args

from api import rest_api, jwt, redis_db

from schemas.sign_in_schema import SignInSchema


@rest_api.route("/auth-token", methods=("POST", "PATCH", "DELETE"))
class AuthToken(Resource):

    redis_namespace = "auth_blacklist"

    @staticmethod
    def authenticate(user):
        access_token = create_access_token(user.email_address, fresh=True)
        refresh_token = create_refresh_token(user.email_address)

        user_info = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        set_access_cookies(user_info, access_token)
        set_refresh_cookies(user_info, refresh_token)
        return user_info

    @classmethod
    @use_args(SignInSchema(), error_status_code=401)
    def post(cls, user):
        return cls.authenticate(user)

    @staticmethod
    @jwt_refresh_token_required
    def patch():  # renews the access token
        access_token = create_access_token(get_jwt_identity())
        set_access_cookies({}, access_token)  # No response required here except a 200.

    @classmethod
    def get_db_key(cls, decoded_refresh_token):
        return f"{cls.redis_namespace}:{decoded_refresh_token['jti']}"

    @classmethod
    @jwt_refresh_token_required
    def delete(cls):
        """
        To take strict security measures, the refresh token is stored into the Redis database and blacklisted.
        Ensures that the refresh token is immediately invalidated despite the fact that it takes a long time to
        expire spontaneously. This will make the JWT not entirely "stateless", but it is a trade-off for security.
        This is not required for the access token as it is short-lived. Also, hitting the database for every request is
        not very efficient.
        """

        refresh_token = get_raw_jwt()["jti"]
        storage_duration = refresh_token["exp"] - int(time())  # time until token expires spontaneously.
        redis_db.set(
            name=cls.get_db_key(refresh_token),
            value=get_jwt_identity(),
            ex=storage_duration
        )
        unset_jwt_cookies({})  # No response required here except a 200.

    # making this a class method messes with jwt as it passes one arg without passing the class.
    @staticmethod
    @jwt.token_in_blacklist_loader
    def is_token_revoked(refresh_token):
        key = AuthToken.get_db_key(refresh_token)
        return redis_db.get(key) is not None
