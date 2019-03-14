from flask import url_for

from flask_jwt_extended import decode_token

from pytest import mark, fixture

from api.auth_token import AuthToken

from models.user import User

from tests.utils.model_instance import model_instance


def get_cookie(client, cookie_name):
    """
    Werkzeug has no method to get a cookie with a particular name from the cookie jar.
    """

    for cookie in client.cookie_jar:
        if cookie.name == cookie_name:
            return cookie


def get_access_token(client):
    return get_cookie(client, "access_token_cookie").value


def get_refresh_token(client):
    return get_cookie(client, "refresh_token_cookie").value


def get_csrf_refresh_token(client):
    return get_cookie(client, "csrf_refresh_token").value


@mark.usefixtures("database", "redis_database")
class TestAuthToken:

    endpoint = "api.auth_token"

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

    def test_post_res_sets_required_auth_and_csrf_cookies(self, post_res, client):
        assert post_res.status_code == 200
        expected_cookies = (
            "access_token_cookie",
            "csrf_access_token",
            "refresh_token_cookie",
            "csrf_refresh_token"
        )
        for cookie in client.cookie_jar:
            assert cookie.name in expected_cookies

    @mark.usefixtures("post_res")
    def test_patch_res_sets_new_access_token_cookie(self, client):
        access_cookie = get_access_token(client)
        refresh_cookie = get_refresh_token(client)
        csrf_refresh_token = get_csrf_refresh_token(client)

        res = client.patch(
            url_for(self.endpoint),
            headers={"X-CSRF-TOKEN": csrf_refresh_token}
        )
        assert res.status_code == 200

        assert access_cookie != get_access_token(client)
        assert refresh_cookie == get_refresh_token(client)

    @mark.usefixtures("post_res")
    def test_delete_res_destroys_all_auth_and_csrf_cookies_and_invalidates_refresh_token(self, client):
        refresh_token = get_refresh_token(client)
        csrf_refresh_token = get_csrf_refresh_token(client)
        res = client.delete(
            url_for(self.endpoint),
            headers={"X-CSRF-TOKEN": csrf_refresh_token}
        )

        assert res.status_code == 200
        for cookie in client.cookie_jar:
            assert cookie.value == ""
        assert AuthToken.is_token_revoked(
            decode_token(refresh_token)
        )
