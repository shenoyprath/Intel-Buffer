from flask import url_for

from models.user import User

from pytest import mark


# file named test_api_user to avoid pytest conflict with test_user from unit/models.
@mark.usefixtures("database")
class TestUser:

    endpoint = "api.user"

    def test_post_res_creates_new_user_and_returns_user_info(self, client, valid_user_info):
        post_res = client.post(
            url_for(self.endpoint),
            data=valid_user_info
        )
        user_info = ("id", "first_name", "last_name")
        for info in user_info:
            assert info in post_res.json
        assert User.get_or_none_by_id(post_res.json["id"])
