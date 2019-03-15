from flask import url_for

from flask_jwt_extended import decode_token

from werkzeug.http import parse_cookie

from api.auth_token import AuthToken

from models.user import User

from pytest import fixture, mark

from tests.utils.model_instance import model_instance


def get_cookie(response, name):
    cookie_headers = response.headers.getlist("Set-Cookie")
    for cookie_header in cookie_headers:
        cookie_dict = parse_cookie(cookie_header)
        cookie_name, = list(cookie_dict.keys())
        if cookie_name == name:
            return cookie_dict[cookie_name]


@mark.usefixtures("database", "redis_database")
class TestAuthToken:

    endpoint = "api.auth_token"

    expected_cookies = (
        "access_token_cookie",
        "csrf_access_token",
        "refresh_token_cookie",
        "csrf_refresh_token"
    )

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
            yield res

    def test_post_response_has_necessary_auth_token_and_csrf_cookie_headers(self, post_res):
        assert post_res.status_code == 200

        for cookie in self.expected_cookies:
            assert get_cookie(post_res, cookie)

    def test_patch_response_renews_access_token_cookie(self, post_res, client):
        access_token = get_cookie(post_res, "access_token_cookie")
        refresh_csrf = get_cookie(post_res, "csrf_refresh_token")

        patch_res = client.patch(
            url_for(self.endpoint),
            headers={"X-CSRF-TOKEN": refresh_csrf}
        )
        assert patch_res.status_code == 200
        assert access_token != get_cookie(patch_res, "access_token_cookie")

    def test_delete_response_deletes_token_cookies_and_revokes_refresh_token(self, post_res, client):
        refresh_token = get_cookie(post_res, "refresh_token_cookie")
        refresh_csrf = get_cookie(post_res, "csrf_refresh_token")

        delete_res = client.delete(
            url_for(self.endpoint),
            headers={"X-CSRF-TOKEN": refresh_csrf}
        )
        assert delete_res.status_code == 200
        for cookie in self.expected_cookies:
            assert get_cookie(delete_res, cookie) == ""
        assert AuthToken.is_token_revoked(
            decode_token(refresh_token)
        )
