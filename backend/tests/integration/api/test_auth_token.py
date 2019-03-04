from flask import url_for

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

from pytest import mark, fixture, raises

from api.auth_token import AuthToken

from models.user import User

from tests.utils.model_instance import model_instance


@mark.usefixtures("database")
class TestAuthToken:

    endpoint = "api.auth_token"

    @mark.usefixtures("client")
    def test_serialization_fails_for_multiple_tokens_of_same_type(self):
        access_tokens = (
            create_access_token("foo"),
            create_access_token("bar")
        )
        refresh_tokens = (
            create_refresh_token("foo"),
            create_refresh_token("bar")
        )

        for same_tokens in (access_tokens, refresh_tokens):
            with raises(TypeError):
                AuthToken.serialize(*same_tokens)

    @fixture
    def post_res(self, client, valid_user_info):
        with model_instance(User, **valid_user_info):
            res = client.post(
                url_for(self.endpoint),
                data=dict(
                    email_address=valid_user_info["email_address"],
                    password=valid_user_info["password"]
                )
            )
        return res

    def test_post_res_has_access_and_refresh_tokens(self, post_res):
        assert post_res.status_code == 200
        assert post_res.json.get("access_token")
        assert post_res.json.get("refresh_token")

    @staticmethod
    def get_auth_header(token):
        return {"Authorization": f"Bearer {token}"}

    @fixture
    def patch_res(self, client, post_res):
        refresh_token = post_res.json["refresh_token"]
        return client.patch(
            url_for(self.endpoint),
            headers=self.get_auth_header(refresh_token)
        )

    @mark.usefixtures("redis_database")
    def test_patch_res_has_access_token_only(self, patch_res):
        assert patch_res.status_code == 200
        assert patch_res.json.get("access_token")
        try:
            patch_res.json["refresh_token"]
        except KeyError:
            pass

    @mark.usefixtures("redis_database")
    def test_access_tokens_have_refresh_token_info_in_claims(self, post_res, patch_res):
        for res in (post_res, patch_res):
            access_token = decode_token(res.json["access_token"])
            claims = access_token["user_claims"]

            refresh_token_key = "refresh_token"
            assert refresh_token_key in claims
            assert "jti" in claims[refresh_token_key]
            assert "exp" in claims[refresh_token_key]

    @mark.usefixtures("redis_database")
    def test_delete_invalidates_access_and_refresh_tokens(self, client, post_res):
        access_token = post_res.json["access_token"]
        decoded_access_token = decode_token(access_token)
        decoded_refresh_token = decode_token(post_res.json["refresh_token"])

        for token in (decoded_access_token, decoded_refresh_token):
            assert not AuthToken.is_token_revoked(token)

        res = client.delete(
            url_for("api.auth_token"),
            headers=TestAuthToken.get_auth_header(access_token)
        )
        assert res.status_code == 200

        for token in (decoded_access_token, decoded_refresh_token):
            assert AuthToken.is_token_revoked(token)
