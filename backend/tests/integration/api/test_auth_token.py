import json

from flask import url_for

from pytest import mark

from models.user import User

from tests.utils.model_instance import model_instance


@mark.usefixtures("database")
class TestAuthToken:
    @staticmethod
    def check_if_response_has_auth_tokens(response):
        json_response = json.loads(response.data)
        assert json_response.get("access_token")
        assert json_response.get("refresh_token")

    @classmethod
    def test_post_returns_access_and_refresh_tokens(cls, client, valid_user_info):
        with model_instance(User, **valid_user_info):
            response = client.post(
                url_for("api.auth_token"),
                data=dict(
                    email_address=valid_user_info["email_address"],
                    password=valid_user_info["password"]
                )
            )

        assert response.status_code == 200
        cls.check_if_response_has_auth_tokens(response)
