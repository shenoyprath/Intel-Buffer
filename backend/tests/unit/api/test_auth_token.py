import json

from flask import url_for

from hypothesis import given
from hypothesis.strategies import emails, text

from models.user import User

from tests.unit.models.model_instance import model_instance


class TestAuthToken:
    @given(
        email_address=emails(),
        password=text(min_size=1)
    )
    def test_post_returns_access_and_refresh_tokens(self, client, email_address, password):
        with model_instance(
            User,
            first_name="John",
            last_name="Doe",
            email_address=email_address,
            password=password
        ):
            response = client.post(
                url_for("api.auth_token"),
                data=dict(email_address=email_address, password=password)
            )

        assert response.status_code == 200

        json_response = json.loads(response.data)
        assert json_response.get("access_token")
        assert json_response.get("refresh_token")
