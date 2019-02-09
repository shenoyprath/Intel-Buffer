from string import printable

from hypothesis import given, example
from hypothesis.strategies import text, dictionaries, recursive, booleans, floats, lists

from pytest import raises

from marshmallow import ValidationError

from models.user import User

from schemas.registration_schema import RegistrationSchema


class TestRegistrationSchema:
    json_strategy = recursive(booleans() |
                              floats() |
                              text(printable),
                              lambda children: lists(children, 1) |
                              dictionaries(text(printable), children, min_size=1))  # straight out of the docs

    required_msg = RegistrationSchema.custom_errors["required"]

    password_len_msg = RegistrationSchema.password_len_msg \
                                         .format(min=User.min_password_len, max=User.max_password_len)

    @staticmethod
    @given(payload=json_strategy)
    @example({})
    def test_invalidates_nonexistence_of_required_fields(payload):
        with raises(ValidationError) as e:
            RegistrationSchema().load(payload)

        required_msg = TestRegistrationSchema.required_msg
        if isinstance(payload, dict):
            assert e.value.messages == {"email_address": [required_msg],
                                        "password": [required_msg],
                                        "first_name": [required_msg],
                                        "last_name": [required_msg]}
        else:
            assert e.value.messages == {"_schema": ["Invalid input type."]}

    @staticmethod
    def test_invalidates_empty_or_whitespace_names():
        pass

    @staticmethod
    @given(password=text(min_size=User.max_password_len + 1))
    def test_invalidates_long_passwords(password):
        password_dict = {"password": password}
        with raises(ValidationError) as e:
            RegistrationSchema().load(password_dict)

        assert "password" in e.value.messages
        assert e.value.messages["password"] == [TestRegistrationSchema.password_len_msg]

    @staticmethod
    @given(password=text(max_size=User.min_password_len - 1))
    def test_invalidates_short_passwords(password):
        password_dict = {"password": password}
        with raises(ValidationError) as e:
            RegistrationSchema().load(password_dict)

        assert "password" in e.value.messages
        assert e.value.messages["password"] == [TestRegistrationSchema.password_len_msg]

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
