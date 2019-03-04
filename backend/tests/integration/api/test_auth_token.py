from flask import url_for

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

from pytest import mark, fixture, raises

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

    @mark.usefixtures("client")
    def test_serialization_fails_when_multiple_tokens_of_same_type_provided(self):
        access_tokens = (
            create_access_token("token1"),
            create_access_token("token2")
        )
        refresh_tokens = (
            create_refresh_token("token1"),
            create_refresh_token("token2")
        )

        for same_tokens in (access_tokens, refresh_tokens):
            with raises(TypeError):
                AuthToken.serialize(*same_tokens)

    def test_post_returns_access_and_refresh_tokens(self, post_response):
        assert post_response.status_code == 200
        assert post_response.json.get("access_token")
        assert post_response.json.get("refresh_token")

    @staticmethod
    def verify_refresh_claims(access_token):
        claims = access_token["user_claims"]

        refresh_token_key = "refresh_token"
        assert refresh_token_key in claims
        assert "jti" in claims[refresh_token_key]
        assert "exp" in claims[refresh_token_key]

    def test_post_created_access_token_has_refresh_token_info_in_claims(self, post_response):
        access_token = decode_token(post_response.json["access_token"])
        self.verify_refresh_claims(access_token)

    @fixture
    def patch_response(self, client, post_response):
        refresh_token = post_response.json["refresh_token"]
        return client.patch(
            url_for("api.auth_token"),
            headers={"Authorization": f"Bearer {refresh_token}"}
        )

    @mark.usefixtures("redis_database")
    def test_patch_returns_new_access_token_only(self, patch_response):
        assert patch_response.status_code == 200
        assert patch_response.json.get("access_token")
        assert patch_response.json.get("refresh_token") is None

    @mark.usefixtures("redis_database")
    def test_patch_created_access_token_has_refresh_token_info_in_claims(self, patch_response):
        access_token = decode_token(patch_response.json["access_token"])
        self.verify_refresh_claims(access_token)

    @mark.usefixtures("redis_database")
    def test_delete_invalidates_access_and_refresh_tokens(self, client, post_response):
        access_token = post_response.json["access_token"]

        def send_delete_request():
            return client.delete(
                url_for("api.auth_token"),
                headers={"Authorization": f"Bearer {access_token}"}
            )

        assert send_delete_request().status_code == 200

        # send delete request again with revoked token
        response = send_delete_request()
        assert response.status_code == 401
        assert response.json["msg"] == "Token has been revoked"

        # assert that refresh token is revoked
        decoded_refresh_token = decode_token(post_response.json["refresh_token"])
        assert redis_db.get(
            AuthToken.get_db_key(decoded_refresh_token)
        )
