from hypothesis import given, example
from hypothesis.strategies import characters, text

from utils.remove_extra_spaces import remove_extra_spaces


class TestRemoveExtraSpaces:
    simple_example = "\tsome  string\n"  # notice 2 spaces between the words

    @staticmethod
    @given(string=text())
    @example(simple_example)
    def test_strips(string):
        result_val = remove_extra_spaces(string)
        if result_val:
            assert not result_val[0].isspace()
            assert not result_val[-1].isspace()

    @staticmethod
    @given(string=text(characters(whitelist_categories=["C", "Z"])))
    @example(simple_example)
    def test_removes_extra_whitespace(string):
        result = remove_extra_spaces(string)
        # check if result has consecutive spaces
        assert not any(result[index].isspace() and
                       result[index + 1].isspace()
                       for index in range(len(result) - 1))
