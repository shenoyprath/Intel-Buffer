from pytest import raises

from marshmallow import ValidationError

from schemas.forbid_blank_str import ForbidBlankStr


class TestForbidBlankStr:
    def test_invalidates_empty_str(self):
        validator = ForbidBlankStr()
        with raises(ValidationError):
            validator("")
