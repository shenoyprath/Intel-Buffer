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
