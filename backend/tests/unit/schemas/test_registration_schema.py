from string import printable

from hypothesis import given, example
from hypothesis.strategies import text, dictionaries, recursive, booleans, floats, lists

from pytest import raises

from marshmallow import ValidationError

from schemas.registration_schema import RegistrationSchema


class TestRegistrationSchema:
    json_strategy = recursive(booleans() |
                              floats() |
                              text(printable),
                              lambda children: lists(children, 1) |
                              dictionaries(text(printable), children, min_size=1))

    @staticmethod
    @given(payload=json_strategy)
    @example({})
    def test_invalidates_if_required_fields_not_provided(payload):
        with raises(ValidationError) as e:
            RegistrationSchema().load(payload)

        if isinstance(payload, dict):
            assert e.value.messages == {"email_address": ["This field is required."],
                                        "password": ["This field is required."],
                                        "first_name": ["This field is required."],
                                        "last_name": ["This field is required."]}
        else:
            assert e.value.messages == {"_schema": ["Invalid input type."]}

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
