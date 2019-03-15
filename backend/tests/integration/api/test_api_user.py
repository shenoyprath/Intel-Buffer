from flask import url_for

from pytest import mark


# file named test_api_user to avoid pytest conflict with test_user from unit/models.
@mark.usefixtures("database")
class TestUser:

    endpoint = "api.user"

    def test_post_res_has_info_of_newly_register_user(self, client, valid_user_info):
        post_res = client.post(
            url_for(self.endpoint),
            data=valid_user_info
        )
        user_info = ("id", "first_name", "last_name")
        for info in user_info:
            assert info in post_res.json
