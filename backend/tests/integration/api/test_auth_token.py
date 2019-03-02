import json

from flask import url_for

from flask_jwt_extended import decode_token

from pytest import mark, fixture

from api import redis_db
from api.auth_token import AuthToken

from models.user import User

from tests.utils.model_instance import model_instance


@mark.usefixtures("database")
class TestAuthToken:
    @fixture
    def post_response(self, client, valid_user_info):
        with model_instance(User, **valid_user_info):
            response = client.post(
                url_for("api.auth_token"),
                data=dict(
                    email_address=valid_user_info["email_address"],
                    password=valid_user_info["password"]
                )
            )
        return response

    def test_post_returns_access_and_refresh_tokens(self, post_response):
        assert post_response.status_code == 200
        json_response = json.loads(post_response.data)
        assert json_response.get("access_token")
        assert json_response.get("refresh_token")

    def test_created_access_token_has_refresh_token_info_in_claims(self, post_response):
        json_response = json.loads(post_response.data)
        access_token = decode_token(json_response["access_token"])
        claims = access_token["user_claims"]

        refresh_token_key = "refresh_token"
        assert refresh_token_key in claims
        assert "jti" in claims[refresh_token_key]
        assert "exp" in claims[refresh_token_key]

    def test_delete_invalidates_access_and_refresh_tokens(self, client, post_response):
        post_response = json.loads(post_response.data)
        access_token = post_response["access_token"]

        def send_delete_request():
            return client.delete(
                url_for("api.auth_token"),
                headers={"Authorization": f"Bearer {access_token}"}
            )

        assert send_delete_request().status_code == 200

        # send delete request again with revoked token
        response = send_delete_request()
        json_response = json.loads(response.data)
        assert response.status_code == 401
        assert json_response["msg"] == "Token has been revoked"

        # assert that refresh token is revoked
        decoded_refresh_token = decode_token(post_response["refresh_token"])
        assert redis_db.get(
            AuthToken.get_db_key(decoded_refresh_token)
        )
