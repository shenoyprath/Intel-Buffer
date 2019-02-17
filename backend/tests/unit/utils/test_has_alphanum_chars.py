from hypothesis import given
from hypothesis.strategies import text, characters

from utils.has_alphanum_chars import has_alphanum_chars


class TestHasAlphanumChars:
    @given(
        string=text(characters(blacklist_categories=("L",)))
    )
    def test_false_if_letters_missing(self, string):
        assert not has_alphanum_chars(string)

    @given(
        string=text(characters(blacklist_categories=("N",)))
    )
    def test_false_if_numbers_missing(self, string):
        assert not has_alphanum_chars(string)
