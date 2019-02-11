from hypothesis import given, example
from hypothesis.strategies import characters, text

from utils.remove_extra_spaces import remove_extra_spaces


class TestRemoveExtraSpaces:
    simple_example = "\tsome  string\n"  # notice 2 spaces between the words

    @staticmethod
    @given(string=text())
    @example(simple_example)
    def test_strips(string):
        result = remove_extra_spaces(string)
        try:
            assert not (result[0].isspace() and result[-1].isspace())
        except IndexError:
            assert not result

    @staticmethod
    @given(string=text(characters(whitelist_categories=["C", "Z"])))  # most whitespace is categorized as either C or Z.
    @example(simple_example)
    def test_removes_extra_whitespace(string):
        result = remove_extra_spaces(string)
        # check if result has consecutive spaces
        assert not any(result[index].isspace() and
                       result[index + 1].isspace()
                       for index in range(len(result) - 1))
