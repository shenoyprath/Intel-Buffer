from string import whitespace

from hypothesis import given, example
from hypothesis.strategies import text, characters

from pytest import raises, fail

from marshmallow import ValidationError
from marshmallow.fields import Field

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

    @given(
        string=text(
            characters(
                whitelist_categories=(),
                whitelist_characters=tuple(whitespace)
            )
        )
    )
    def test_invalidates_whitespace_str(self, string):
        validator = ForbidBlankStr(forbid_whitespace_str=True)
        with raises(ValidationError):
            validator(string)

    @given(error=text())
    @example("")
    def test_invalidates_with_correct_error(self, error):
        validator = ForbidBlankStr(error=error)
        with raises(ValidationError) as e:
            validator("")

        if error:
            assert error in e.value.messages
        else:
            assert Field.default_error_messages["required"] in e.value.messages
