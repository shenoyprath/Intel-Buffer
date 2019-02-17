from pytest import raises, fail

from marshmallow import ValidationError

from schemas.forbid_blank_str import ForbidBlankStr


class TestForbidBlankStr:
    def test_invalidates_empty_str(self):
        validator = ForbidBlankStr()
        with raises(ValidationError):
            validator("")

    def test_validates_none(self):
        validator = ForbidBlankStr()
        try:
            validator(None)
        except ValidationError as e:
            fail(f"ValidationError was unexpectedly raised when validating None: \n{str(e)}")
