from werkzeug.exceptions import BadRequest

from marshmallow import ValidationError

from pytest import raises

from hypothesis import given
from hypothesis.strategies import text

from api.error_handler import handle_error


class TestErrorHandler:
    @given(error_msg=text())
    def test_handle_error(self, error_msg):
        with raises(BadRequest):
            handle_error(
                error=ValidationError(error_msg),
                _request=None,
                _schema=None,
                status_code=400,
                _error_headers=None
            )
