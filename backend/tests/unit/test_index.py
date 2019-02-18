from flask import url_for

from pytest import fixture


class TestIndex:
    @fixture
    def index_response(self, client):
        return client.get(
            url_for("index")
        )

    def test_responds_200(self, index_response):
        assert index_response.status_code == 200

    def test_sends_html_file(self, index_response):
        assert index_response.content_type == "text/html; charset=utf-8"

        assert (
            b"We're sorry but IntelBuffer doesn't work properly "
            b"without JavaScript enabled. "
            b"Please enable it to continue."
        ) in index_response.data
        assert b"<div id=app></div>" in index_response.data
