from flask import url_for

from pytest import mark


# file named test_api_user to avoid pytest conflict with test_user from unit/models.
@mark.usefixtures("database")
class TestUser:
    def test_post_res_has_access_and_refresh_tokens(self, client, valid_user_info):
        res = client.post(
            url_for("api.user"),
            data=valid_user_info
        )

        assert res.status_code == 200
        assert res.json.get("access_token")
        assert res.json.get("refresh_token")
