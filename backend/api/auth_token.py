from datetime import datetime

from flask import jsonify

from flask_restplus import Resource

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, \
                               get_jwt_claims, get_raw_jwt

from webargs.flaskparser import use_args

from api import rest_api, jwt, redis_db

from schemas.login_schema import LoginSchema


@rest_api.route("/auth_token", methods=("POST",))
class AuthToken(Resource):

    redis_blacklist_namespace = "token_blacklist:"

    @staticmethod
    @jwt.user_claims_loader
    def add_token_claims(identity):
        """
        Custom claims for the authentication tokens (mostly to find the time the token was issued at).
        """

        return {"identity": identity,
                "creation_timestamp": str(datetime.utcnow())}

    @staticmethod
    @use_args(LoginSchema(), error_status_code=401)
    def post(args):
        """
        Creates a new authentication (access and refresh) token for the client.
        """

        email_address = args.get("email_address")

        access_token = create_access_token(email_address)
        refresh_token = create_refresh_token(email_address)

        response = jsonify(access_token=access_token, refresh_token=refresh_token)
        response.status_code = 200
        return response

    @staticmethod
    @jwt.token_in_blacklist_loader
    def is_token_blacklisted(jwt_dict):
        user_email_address = jwt_dict.get("jti")  # jti stores the identity
        return redis_db.get(f"{AuthToken.redis_blacklist_namespace}"
                            f"{user_email_address}") is not None

    @staticmethod
    @jwt_required
    def delete():
        """
        Blacklists the client's authentication tokens till it expires. Used to "log the client out".
        No way to avoid state management here because token needs to be invalidated immediately.
        """

        token_expiration = get_jwt_claims().get("creation_timestamp")
        expiration_delta = datetime.utcnow() - datetime.strptime(token_expiration, "%Y-%m-%d %H:%M:%S.%f")

        redis_db.set(name=f"{AuthToken.redis_blacklist_namespace}"
                          f"{get_jwt_identity()}",
                     value=get_raw_jwt(),
                     ex=expiration_delta.total_seconds())
