from string import whitespace

from hypothesis import given
from hypothesis.strategies import text, characters

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

    @given(string=text(characters(whitelist_categories=(),
                                  whitelist_characters=list(whitespace))))
    def test_invalidates_whitespace_str(self, string):
        validator = ForbidBlankStr(forbid_whitespace_str=True)
        with raises(ValidationError):
            validator(string)
