from flask import url_for

from pytest import mark


# file named test_api_user to avoid pytest conflict with test_user from unit/models.
@mark.usefixtures("database")
class TestUser:
    def test_post_returns_auth_tokens(self, client, valid_user_info):
        response = client.post(
            url_for("api.user"),
            data=valid_user_info
        )

        assert response.status_code == 200
        assert response.json.get("access_token")
        assert response.json.get("refresh_token")
