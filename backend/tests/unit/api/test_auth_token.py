import json

from flask import url_for

from models.user import User

from tests.unit.models.model_instance import model_instance


class TestAuthToken:
    def test_post_returns_access_and_refresh_tokens(self, client):
        dummy_email = "example@example.com"
        dummy_password = "Password123"
        with model_instance(
            User,
            first_name="John",
            last_name="Doe",
            email_address=dummy_email,
            password=dummy_password
        ):
            response = client.post(
                url_for("api.auth_token"),
                data=dict(email_address=dummy_email, password=dummy_password)
            )

        assert response.status_code == 200

        json_response = json.loads(response.data)
        assert json_response.get("access_token")
        assert json_response.get("refresh_token")
