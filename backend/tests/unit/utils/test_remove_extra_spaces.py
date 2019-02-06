from hypothesis import given, example
from hypothesis.strategies import text, iterables

from utils.remove_extra_spaces import remove_extra_spaces


class TestRemoveExtraSpaces:
    initial_val_example = "\tsome  string\n"  # notice 2 spaces between the words

    @staticmethod
    @given(string=text())
    @example(initial_val_example)
    def test_strips(string):
        result_val = remove_extra_spaces(string)
        if result_val:
            assert not result_val[0].isspace()
            assert not result_val[-1].isspace()

    @staticmethod
    def has_consecutive_spaces(string):
        for index in range(len(string) - 1):
            if string[index].isspace() and string[index + 1].isspace():
                return True
        return False

    @staticmethod
    @given(string=text())
    @example(initial_val_example)
    def test_removes_extra_whitespace(string):
        result_val = remove_extra_spaces(string)
        assert not TestRemoveExtraSpaces.has_consecutive_spaces(result_val)

    @staticmethod
    @given(strings=iterables(text()))
    @example([initial_val_example, "\t\n\r"])
    def test_removes_extra_whitespace_for_multiple(strings):
        result_val = remove_extra_spaces(*strings)
        for val in result_val:
            assert not TestRemoveExtraSpaces.has_consecutive_spaces(val)
