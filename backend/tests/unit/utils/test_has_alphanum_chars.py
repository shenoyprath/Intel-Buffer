from string import ascii_letters, digits

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

    @given(
        letters=text(
            characters(
                whitelist_categories=(),
                whitelist_characters=tuple(ascii_letters)
            ),
            min_size=1
        ),
        numbers=text(
            characters(
                whitelist_categories=(),
                whitelist_characters=tuple(digits)
            ),
            min_size=1
        )
    )
    def test_true_if_letters_and_numbers_present(self, letters, numbers):
        string = letters + numbers
        assert has_alphanum_chars(string)
