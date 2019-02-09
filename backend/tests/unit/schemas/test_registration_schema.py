import json
from string import printable

from hypothesis.strategies import text, dictionaries, recursive, booleans, floats, lists


class TestRegistrationSchema:
    json_strategy = recursive(booleans() |
                              floats() |
                              text(printable),
                              lambda children: lists(children, 1) |
                              dictionaries(text(printable), children, min_size=1))

    empty_json = json.loads(json.dumps({}))

    @staticmethod
    def test_invalidates_blank_fields():
        pass

    @staticmethod
    def test_invalidates_just_whitespace_names():
        pass

    @staticmethod
    def test_invalidates_long_passwords():
        pass

    @staticmethod
    def test_invalidates_short_passwords():
        pass

    @staticmethod
    def test_invalidates_password_without_letters():
        pass

    @staticmethod
    def test_invalidates_password_without_nums():
        pass

    @staticmethod
    def test_invalidates_password_matching_email():
        pass

    @staticmethod
    def test_validates_when_all_criteria_meet():
        pass
